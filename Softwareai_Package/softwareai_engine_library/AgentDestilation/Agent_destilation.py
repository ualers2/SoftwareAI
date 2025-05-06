#########################################
# IMPORT SoftwareAI Libs 
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################

class Agent_destilation:
    """
    Responsible for logging agent interactions (input, output, instructions) into JSON and JSONL files,
    organized by date and assistant name.
    """
                                                
    def DestilationResponseAgent(input, output, instructionsassistant, nameassistant):                        
        """
        Destilação de agentes, com essa funcao voce pode armazenar todos os input, output e instructionsassistant
        """ 
        date = datetime.now().strftime('%Y-%m-%d')
        datereplace = date.replace('-', '_').replace(':', '_')
        output_path_jsonl = os.path.abspath(os.path.join(os.path.dirname(__file__), "Destilation", f'{nameassistant}', "Jsonl", f'DestilationAgent{datereplace}'))
        output_path_json = os.path.abspath(os.path.join(os.path.dirname(__file__), "Destilation", f'{nameassistant}', "Json", f'DestilationAgent{datereplace}'))
        output_path_json2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "Destilation", f'{nameassistant}', "Jsonl_2", f'DestilationAgent{datereplace}', f"DestilationDateTime_{datereplace}.json"))
        os.makedirs(output_path_json, exist_ok=True)
        os.makedirs(os.path.dirname(output_path_json2), exist_ok=True)
        os.makedirs(output_path_jsonl, exist_ok=True)
            
        datasetjson = {
            "input": input,
            "output": output
        }

        try:
            with open(output_path_json2, 'x', encoding='utf-8') as json_file:
                json_file.close()
        except:
            pass

        new_entry = {"input": input, "output": output}

        # Verificando se o arquivo já existe e lendo os dados
        if os.path.exists(output_path_json2):
            with open(output_path_json2, 'r', encoding='utf-8') as json_file:
                try:
                    datasetjson2 = json.load(json_file)  # Carregar o JSON existente
                    if not isinstance(datasetjson2, list):
                        datasetjson2 = []  # Se não for uma lista, inicializar como lista
                except json.JSONDecodeError:
                    datasetjson2 = []  # Inicializar lista se o arquivo estiver vazio ou corrompido
        else:
            datasetjson2 = []  # Inicializar lista se o arquivo não existir

        datasetjson2.append(new_entry)

        with open(output_path_json2, 'w', encoding='utf-8') as json_file:
            json.dump(datasetjson2, json_file, indent=4, ensure_ascii=False)
                



        datasetjsonl = {
            "messages": [
                {"role": "system", "content": f"{instructionsassistant}"},
                {"role": "user", "content": f"{input}"},
                {"role": "assistant", "content": f"{output}"}
            ]
        }

        finaloutputjson = os.path.join(output_path_json, f"DestilationDateTime_{datereplace}.json")
        with open(finaloutputjson, 'a', encoding='utf-8') as json_file:
            json.dump(datasetjson, json_file, indent=4, ensure_ascii=False)


        finaloutputjsonl = os.path.join(output_path_jsonl, f"DestilationDateTime_{datereplace}.jsonl")
        with open(finaloutputjsonl, 'a', encoding='utf-8') as json_file:
            json_file.write(json.dumps(datasetjsonl, ensure_ascii=False) + "\n")
        
        return True
