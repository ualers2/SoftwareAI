from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


# from CodeUploadGit.UploadGit import CodeUploadGit

from Agents.Code.BackEnd.api_login.Integration import CodeFlaskBackEndSprint8Agent

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeFlaskBackEndSprint7Agent: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeFlaskBackEndSprint7Agent(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")
    session_id_CodeFlaskBackEndSprint8Agent = "teste_handoff_CodeFlaskBackEndSprint8Agent"
    agent_, handoff_obj_CodeFlaskBackEndSprint8Agent = CodeFlaskBackEndSprint8Agent(session_id_CodeFlaskBackEndSprint8Agent, appcompany)

   
    api_register = '''
```python
@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    SUBSCRIPTION_PLAN = data.get("SUBSCRIPTION_PLAN")
    expiration = data.get("expiration")
    WEBHOOK_SECRET_flag = data.get("WEBHOOK_SECRET_flag")
    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400
    if not SUBSCRIPTION_PLAN:
        SUBSCRIPTION_PLAN = "free"
    if not expiration:
        expiration = "None"
    if SUBSCRIPTION_PLAN == "free":
        limit = "2 per day"
    elif SUBSCRIPTION_PLAN == "premium":
        limit = "50 per day"

    email_safe = email.replace('.', '_')
    ref = db.reference(f'users/{email_safe}', app=appcompany)
    if ref.get():
        if not WEBHOOK_SECRET_flag:
            return jsonify({"error": "Voce ja tem uma conta"}), 400
        
        if WEBHOOK_SECRET_flag == WEBHOOK_SECRET:
                
            api_key = generate_api_key(SUBSCRIPTION_PLAN)

            ref.update({
                "api_key": api_key
            })
            ref.update({
                "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN
            })
            ref.update({
                "limit": limit
            })
            ref.update({
                "expiration": expiration
            })

            return jsonify({"message": "Upgrade realizado",
                            "email": email,
                            "password": password,
                            "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
                            "limit": limit,
                            "expiration": expiration,
                            "api_key": api_key,
                        }), 409
            
    api_key = generate_api_key(SUBSCRIPTION_PLAN)

    ref.set({
        "email": email,
        "password": password,
        "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
        "limit": limit,
        "expiration": expiration,
        "api_key": api_key,
        "stripe_account_id": "None",
        'created_at': datetime.now().isoformat()
        
    })
    return jsonify({
        "message": "Usuário registrado com sucesso",
        "email": email,
        "password": password,
        "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
        "limit": limit,
        "expiration": expiration,
        "api_key": api_key,
        "stripe_account_id": "None",
        'created_at': datetime.now().isoformat()
        
        }), 200
```


    '''
   
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
        handoffs=[handoff_obj_CodeFlaskBackEndSprint8Agent],




    )

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj