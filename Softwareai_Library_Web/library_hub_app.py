# import time

# while True:
#    time.sleep(67789)


from flask import Flask, render_template, request, redirect, url_for, session, jsonify, make_response, Response
from flask_cors import CORS
from datetime import timedelta
import os
import json
import yaml
from dotenv import load_dotenv
import logging
import sys
import importlib.util
import inspect
import zipfile
import io



from modules.services.load_agents import load_agents_from_firebase
from modules.modules import *
from modules.get_agent_metadata import get_agent_metadata
from modules.calculate_tool_hash import *
from modules.register_tool_version import *
from modules.calculate_agent_hash import calculate_agent_hash
from modules.register_agent_version import register_agent_version



app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)  # Isso permite CORS para todas as rotas
app.secret_key = 'sua_chave_secreta' 
app.permanent_session_lifetime = timedelta(minutes=60)  

load_dotenv(dotenv_path="Keys/keys.env")

key_openai = os.getenv("OPENAI_API_KEY")
client = OpenAI(
    api_key=key_openai,
)

path_APPCOMPANY = os.getenv("FIREBASE_CREDENTIALS", "/app/Keys/appcompany.json") 
with open(path_APPCOMPANY) as f:
    firebase_credentials_APPCOMPANY = json.load(f)

credt1 = credentials.Certificate(firebase_credentials_APPCOMPANY)
appcompany = initialize_app(credt1, {
   'databaseURL': os.getenv("FIREBASE_URL")
}, name='appcompany')

AGENTS_DIR = os.path.join(os.path.dirname(__file__), "Agents")
BASE_DIR = os.path.join(os.path.dirname(__file__), 'FunctionsAndTools')
FOLDERS = ['Functions']

# Configura o logger
logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)  # ou INFO, WARNING etc.

# Cria um handler para a saída padrão (stdout)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Formato dos logs
formatter = logging.Formatter(
    fmt='[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Evita adicionar múltiplos handlers
if not logger.hasHandlers():
    logger.addHandler(handler)

@app.context_processor
def inject_static_url():
    return dict(static_url=url_for('static', filename=''))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/index.html')
def index2():
    return render_template('index.html')  

@app.route('/tools.html')
def pagetools():
    return render_template('tools.html')  

@app.route('/tools')
def pagetools2():
    return render_template('tools.html')  

@app.route('/tools/<tool_id>')
def tool_detail(tool_id):
    return render_template('tool_detail.html', tool_id=tool_id)

@app.route('/agent.html')
def serve_agent_page():
    return render_template('agent.html') 

@app.route('/agents')
def serve_agent_page2():
    return render_template('agent.html') 

@app.route('/api/agents/<agent_id>', methods=['GET'])
def get_agent(agent_id):
    try:
        ref = db.reference(f'agents/{agent_id}/metadata')
        metadata = ref.get()

        if not metadata:
            return jsonify({"error": "Agent not found"}), 404

        agent_info = {
            "tutorial": metadata.get("tutorial")
        }

        logger.info(f"agent_id {agent_info}")
        return jsonify(agent_info)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
# @app.route('/api/agents/<agent_id>', methods=['GET'])
# def get_agent(agent_id):
#     agent_path = os.path.join(AGENTS_DIR, agent_id)
#     info_path = os.path.join(agent_path, "info.json")
#     tutorial_path = os.path.join(agent_path, "tutorial.md")

#     if not os.path.exists(info_path):
#         return jsonify({"error": "Agent not found"}), 404

#     with open(info_path, "r", encoding="utf-8") as f:
#         info = json.load(f)

#     if os.path.exists(tutorial_path):
#         with open(tutorial_path, "r", encoding="utf-8") as f:
#             info["tutorial"] = f.read()
#     else:
#         info["tutorial"] = ""
#     logger.info(f"agent_id {info}")
#     return jsonify(info)

@app.route('/api/agents/history', methods=['GET'])
def get_agent_history():
    """
    Retorna todas as versões de um agente, ordenadas por timestamp decrescente.
    Query parameter:
      - agent_id: ID do agente cujas versões serão retornadas.
    """
    agent_id = request.args.get('agent_id')
    if not agent_id:
        return jsonify({'error': 'O parâmetro agent_id é obrigatório.'}), 400

    # Referência à coleção de versões do agente no Firebase
    ref = db.reference(f"agents/{agent_id}/history/versions", app=appcompany)
    snapshot = ref.get() or {}

    # Converte o snapshot (dict) em lista e ordena as versões
    versions = list(snapshot.values())
    versions.sort(key=lambda v: v.get('timestamp', 0), reverse=True)

    return jsonify(versions), 200

@app.route('/api/agents', methods=['GET'])
def get_agents():
    try:
        agents = load_agents_from_firebase(appcompany)
        logger.info(agents)
        return jsonify(agents)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/compose', methods=['GET'])
def get_compose():
    with open("softwareai-compose.yml", "r", encoding="utf-8") as file:
        yaml_data = file.read()
    return Response(yaml_data, mimetype="text/yaml")



@app.route('/api/agent-metadata/<agent_ids>', methods=['GET'])
def agent_metadata(agent_ids):
    agent_ids = agent_ids.split(',')
    metadata = get_agent_metadata(agent_ids, appcompany)
    return jsonify(metadata)

@app.route('/api/tool-metadata/<tool_id>', methods=['GET'])
def get_tool_metadata(tool_id):
    for folder in FOLDERS:
        folder_path = os.path.join(BASE_DIR, folder)
        tool_path = os.path.join(folder_path, tool_id)
        metadata_path = os.path.join(tool_path, 'metadata.json')
        code_path = os.path.join(tool_path, f'{tool_id}.py')  # arquivo Python

        if os.path.isfile(metadata_path):
            try:
                with open(metadata_path, 'r') as f:
                    metadata = json.load(f)
                    
                # Tenta ler o código se existir
                if os.path.isfile(code_path):
                    with open(code_path, 'r', encoding='utf-8') as code_file:
                        metadata["code"] = code_file.read()
                else:
                    metadata["code"] = "# Código não encontrado"

                return jsonify(metadata)
            except Exception as e:
                return jsonify({'error': f'Erro ao ler arquivos: {str(e)}'}), 500

    return jsonify({'error': 'metadata.json não encontrado'}), 404

@app.route('/api/submit-tool-output', methods=['POST'])
def submit_tool_output_endpoint():
    try:
        data = request.get_json()
        function_name = data.get('function_name')
        function_arguments = data.get('function_arguments')
        tool_call = data.get('tool_call')
        thread_id = data.get('thread_id')
        run = data.get('run')
        OPENAI_API_KEY = data.get('OPENAI_API_KEY')
        
        if not all([function_arguments, tool_call, thread_id, run]):
            return jsonify({'error': 'Parâmetros ausentes ou inválidos'}), 400
                

        # reconstruir o objeto de forma mínima
        run = Run(data.get('run', {}).get('id'))

        mappingtool(function_name, function_arguments, tool_call)
        
        submit_output(thread_id,client,run)


        return jsonify({'message': 'Saída da ferramenta enviada com sucesso!'}), 200

    except ValueError as e:
        return jsonify({'error': str(e)}), 400
    except Exception as e:
        return jsonify({'error': f'Erro ao processar a saída da ferramenta: {str(e)}'}), 500

@app.route('/api/list-tools', methods=['GET'])
def list_tools():
    all_tools = []

    for folder in FOLDERS:
        folder_path = os.path.join(BASE_DIR, folder)
        if not os.path.exists(folder_path):
            continue

        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            metadata_path = os.path.join(item_path, 'metadata.json')
            compose_path = os.path.join(item_path, 'tool-compose.yml')

            tool_data = {
                'id': item,
                'type': folder[:-1].lower(),  # 'function' ou 'tool'
                'name': item.replace('_', ' ').title(),
                'icon': 'fas fa-toolbox text-xl',
                'shortDescription': '',
                'fullDescription': '',
                'parameters': {},
            }

            # tool-compose.yml (opcional)
            if os.path.isfile(compose_path):
                try:
                    with open(compose_path, 'r') as f:
                        compose_data = yaml.safe_load(f)
                        compose_info = compose_data.get('tool_compose', {})
                        tool_data.update({
                            'id': compose_info.get('id', item),
                            'type_plan': compose_info.get('type_plan', "free"),
                            'icon': compose_info.get('icon', tool_data['icon']),
                            'shortDescription': compose_info.get('shortDescription', ''),
                            'fullDescription': compose_info.get('fullDescription', ''),
                            'useCases': compose_info.get('UseCases', ''),
                        })
                except Exception as e:
                    print(f"Erro ao ler tool-compose.yml de {item}: {e}")

            # metadata.json (opcional)
            if os.path.isfile(metadata_path):
                try:
                    with open(metadata_path, 'r') as f:
                        metadata = json.load(f)
                        if 'function' in metadata:
                            func = metadata['function']
                            tool_data.update({
                                'name': func.get('name', tool_data['name']),
                                'description': func.get('description', ''),
                                'parameters': func.get('parameters', {}),
                            })
                except Exception as e:
                    print(f"Erro ao ler metadata.json de {item}: {e}")

            all_tools.append(tool_data)

    return jsonify(all_tools)

@app.route('/api/get-tools-by-id', methods=['POST'])
def get_tools_by_id():
    try:
        data = request.get_json()
        requested_ids = data.get('tool_ids', [])

        if not requested_ids or not isinstance(requested_ids, list):
            return jsonify({'error': 'Parâmetro "tool_ids" inválido ou ausente'}), 400

        matched_tools = []

        for folder in FOLDERS:
            folder_path = os.path.join(BASE_DIR, folder)
            if not os.path.exists(folder_path):
                continue

            for tool_id in requested_ids:
                item_path = os.path.join(folder_path, tool_id)
                metadata_path = os.path.join(item_path, 'metadata.json')
                compose_path = os.path.join(item_path, 'tool-compose.yml')

                if not os.path.exists(item_path):
                    continue

                tool_data = {
                    'id': tool_id,
                    'type': folder[:-1].lower(),
                    'name': tool_id.replace('_', ' ').title(),
                    'icon': 'fas fa-toolbox text-xl',
                    'shortDescription': '',
                    'fullDescription': '',
                    'parameters': {},
                }

                # tool-compose.yml
                if os.path.isfile(compose_path):
                    try:
                        with open(compose_path, 'r') as f:
                            compose_data = yaml.safe_load(f)
                            compose_info = compose_data.get('tool_compose', {})
                            tool_data.update({
                                'id': compose_info.get('id', tool_id),
                                'icon': compose_info.get('icon', tool_data['icon']),
                                'shortDescription': compose_info.get('shortDescription', ''),
                                'fullDescription': compose_info.get('fullDescription', ''),
                                'useCases': compose_info.get('UseCases', ''),
                            })
                    except Exception as e:
                        print(f"Erro ao ler tool-compose.yml de {tool_id}: {e}")

                # metadata.json
                if os.path.isfile(metadata_path):
                    try:
                        with open(metadata_path, 'r') as f:
                            metadata = json.load(f)
                            if 'function' in metadata:
                                func = metadata['function']
                                tool_data.update({
                                    'name': func.get('name', tool_data['name']),
                                    'description': func.get('description', ''),
                                    'parameters': func.get('parameters', {}),
                                })
                    except Exception as e:
                        print(f"Erro ao ler metadata.json de {tool_id}: {e}")

                matched_tools.append(tool_data)

        return jsonify(matched_tools)

    except Exception as e:
        return jsonify({'error': f'Erro interno: {str(e)}'}), 500



@app.route('/api/tool-code/<tool_ids>', methods=['GET'])
def get_tool_codes(tool_ids):
    tool_ids_list = tool_ids.split(',')
    zip_buffer = io.BytesIO()

    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for tool_id in tool_ids_list:
            found = False
            for folder in FOLDERS:
                tool_path = os.path.join(BASE_DIR, folder, tool_id)
                if not os.path.exists(tool_path):
                    continue

                # Calcula o novo hash
                new_hash = calculate_tool_hash(tool_path)

                # Verifica se o hash atual é diferente do último registrado
                latest_hash_ref = db.reference(f"tool_hashes/{tool_id}/latest", app=appcompany).get()
                latest_data = db.reference(f"tool_hashes/{tool_id}/versions/{latest_hash_ref}", app=appcompany).get() if latest_hash_ref else None

                if not latest_data or latest_data.get("hash") != new_hash:
                    register_tool_version(tool_id, new_hash, appcompany)

                # Adiciona todos os arquivos .py da ferramenta ao ZIP
                for file in os.listdir(tool_path):
                    if file.endswith('.py'):
                        file_path = os.path.join(tool_path, file)
                        zipf.write(file_path, arcname=f"{tool_id}/{file}")
                        found = True

            if not found:
                return jsonify({'error': f'Nenhum arquivo .py encontrado para a ferramenta "{tool_id}"'}), 404

    zip_buffer.seek(0)
    response = make_response(zip_buffer.read())
    response.headers.set('Content-Type', 'application/zip')
    response.headers.set('Content-Disposition', 'attachment', filename='tools_code.zip')
    return response

@app.route('/api/agent-code/<agent_ids>', methods=['GET'])
def get_agent_codes(agent_ids):
    """
    Gera um ZIP contendo apenas Integration.py e metadata.json de cada agente,
    preservando a estrutura original de subpastas.
    """
    requested = agent_ids.split(',')
    zip_buffer = io.BytesIO()
    
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for agent_id in requested:
            found = False
            seen = set()
            # Retorna tuplas de (root_folder, caminho absoluto do agente)
            for root_folder, agent_root in find_agent_paths(agent_id, AGENTS_DIR, BASE_DIR):
                # Para cada arquivo desejado, calcula caminho dentro do zip como relativo a BASE_DIR
                for dirpath, _, filenames in os.walk(agent_root):
                    if 'Integration.py' in filenames:
                        full_py = os.path.join(dirpath, 'Integration.py')
                        arc_py = os.path.relpath(full_py, BASE_DIR)
                        if arc_py not in seen:
                            zipf.write(full_py, arcname=arc_py)
                            seen.add(arc_py)
                            found = True

                    if 'metadata.json' in filenames:
                        full_meta = os.path.join(dirpath, 'metadata.json')
                        arc_meta = os.path.relpath(full_meta, BASE_DIR)
                        if arc_meta not in seen:
                            zipf.write(full_meta, arcname=arc_meta)
                            seen.add(arc_meta)
                            found = True

            if not found:
                return jsonify({
                    'error': f'Nenhum Integration.py ou metadata.json encontrado para agente "{agent_id}"'
                }), 404

    zip_buffer.seek(0)
    response = make_response(zip_buffer.read())
    response.headers.set('Content-Type', 'application/zip')
    response.headers.set('Content-Disposition', 'attachment', filename='agents_code.zip')
    return response


if __name__ == '__main__': # debug=True, 
    app.run(host="0.0.0.0", port=821)

  