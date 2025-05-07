
import tiktoken
import firebase_admin
from firebase_admin import credentials, db
from typing import Dict, Any
from dotenv import load_dotenv
import os

# Carrega variáveis de ambiente e inicializa Firebase
dotenv_path = os.path.join("Keys", "keys.env")
load_dotenv(dotenv_path=dotenv_path)
firebase_json_path = os.getenv("firebase_json_path")
firebase_db_url = os.getenv("firebase_db_url")

cred = credentials.Certificate(firebase_json_path)
app_instance = firebase_admin.initialize_app(cred, {
    "databaseURL": firebase_db_url
})

agent_ids = [
    "AutonomousValuation",
    "CRM",
    "Checkout",
    "CodeReview_BackEnd_Endpoints",
    "CodeReview_FrontEnd_Html",
    "CodeReview_FrontEnd_JS",
    "CodeReview_Keys",
    "CreateProduct",
    "CreateWebhook",
    "Dashboard_Decision",
    "Dashboard_Learning_Management_Agent",
    "Dashboard_Product_Performance_Agent",
    "Dashboard_Supply_Chain_Agent",
    "DeployProjectModeEasy",
    "DockerBuild",
    "DockerCompose",
    "DockerFile",
    "Git",
    "IA",
    "Index",
    "Keys_env",
    "Login",
    "Modules",
    "NavigationJS",
    "PreProject",
    "RequirementsTxt",
    "ReservationPlatform",
    "RunBuildProject",
    "Scheduling",
    "Staticjs",
    "Technich",
    "Timeline",
    "TranscriptIssue",
    "TypeProject",
    "api_create_checkout",
    "api_login",
    "api_register",
    "basic_endpoints",
    "unittest_login_user_by_ui",
    "unittest_user_checkout_by_ui",
    "unittest_user_created_by_ui",
    "webhook"
]

# Taxas por milhão de tokens
COST_INSTRUCTION_PER_MILLION = 1.10    # US$ por 1 000 000 de tokens de instrução
COST_OUTPUT_PER_MILLION      = 4.40    # US$ por 1 000 000 de tokens de output

# Convertendo para custo unitário
cost_instruction_token = COST_INSTRUCTION_PER_MILLION / 1_000_000
cost_output_token      = COST_OUTPUT_PER_MILLION      / 1_000_000

# Faixa média de output tokens
MIN_OUTPUT_TOKENS = 25_000
MAX_OUTPUT_TOKENS = 45_000
avg_output_tokens = (MIN_OUTPUT_TOKENS + MAX_OUTPUT_TOKENS) / 2 

total_input_tokens  = 0
total_output_tokens = 0
total_cost          = 0.0
total_exception =  0
for agent_id in agent_ids:
    try:
            
        # Busca metadata no Realtime Database
        ref = db.reference(f'agents/{agent_id}/metadata', app=app_instance)
        metadata = ref.get()
        instruction = metadata["instruction"]

        # Encoding dos tokens de instrução
        try:
            enc = tiktoken.encoding_for_model("o3-mini-2025-01-31")
        except KeyError:
            enc = tiktoken.get_encoding("cl100k_base")

        input_tokens = len(enc.encode(instruction))
        total_input_tokens += input_tokens

        # Custo instrução
        cost_instr = input_tokens * cost_instruction_token

        # Cálculo de tokens e custo de output (média)
        output_tokens = avg_output_tokens
        total_output_tokens += output_tokens
        cost_out = output_tokens * cost_output_token

        # Custo total deste agente (input + output)
        cost_agent = round(cost_instr + cost_out, 6)
        total_cost += cost_agent

        # print(f"{agent_id}: instr={input_tokens} tok → ${cost_instr:.6f}  |  "
        #     f"output≈{output_tokens} tok → ${cost_out:.6f}  →  total=${cost_agent}")
    except:
        total_exception += 1 

print("────────────────────────────────────────")
print(f"o AgentsWorkFlow Saas consome {total_input_tokens} Tokens de instrucao")
print(f"o AgentsWorkFlow Saas consome {total_output_tokens} Tokens de output ")
print(f"o Projeto terá o Custo estimado total de : ${total_cost:.6f}")
print(f"o Projeto terá o Custo médio por agente:  ${total_cost/len(agent_ids):.6f}")
print(f"Total de execoes ao buscar agentes {total_exception}")
