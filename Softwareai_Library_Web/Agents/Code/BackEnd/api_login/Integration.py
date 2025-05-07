from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *

# from Agents.Code.BackEnd.Sprint9.Integration import CodeFlaskBackEndSprint9Agent

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeFlaskBackEndSprint8Agent: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeFlaskBackEndSprint8Agent(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"
    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

    # session_id_CodeFlaskBackEndSprint9Agent = "teste_handoff_CodeFlaskBackEndSprint9Agent"
    # agent_, handoff_obj_CodeFlaskBackEndSprint9Agent = CodeFlaskBackEndSprint9Agent(session_id_CodeFlaskBackEndSprint9Agent, appcompany)


    api_login = '''
```python
@app.route('/api/login', methods=['POST'])
def apilogin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    email_safe = email.replace('.', '_')
    user = db.reference(f'users/{email_safe}', app=appcompany).get()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if user["password"] != password:
        return jsonify({"error": "Senha incorreta"}), 401

    session['user'] = email
    session.permanent = True  # <- IMPORTANTE

    return jsonify({"message": "Login realizado com sucesso"}), 200

```
    '''
   
# {RECOMMENDED_PROMPT_PREFIX}\n
# ---

# Ao final de sua execução, utilize o Handoffs transfer_to_code_upload_git_agent
# Ao final de sua execução, Encaminhe o usuário para o agente de Code Upload Git Agent
# prossiga com a criacao do repositorio e o upload dos arquivos da aplicacao 
# Encaminhe ao agente Code Upload Git Agent para criação do repositório e upload 
# dos arquivos da aplicação.
# ---

# voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
# jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

# ---
   
    name_agent, model_agent, instruction_original, tools_agent  = get_settings_agents(path_metadata = os.path.join(os.path.dirname(__file__), "metadata.json"))
    instruction_formatado = format_instruction(instruction_original, locals())

    Tools_Name_dict = Egetoolsv2(list(tools_agent))
    agent = Agent(
        name=name_agent,
        instructions = f"""
{RECOMMENDED_PROMPT_PREFIX}
{instruction_formatado}
        """
        ,
        model=str(model_agent),
        tools=Tools_Name_dict,
        # handoffs=[handoff_obj_CodeFlaskBackEndSprint9Agent],


    )



    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj