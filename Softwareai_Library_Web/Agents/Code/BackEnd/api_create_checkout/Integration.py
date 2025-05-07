from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *


from Agents.Code.BackEnd.webhook.Integration import CodeFlaskBackEndSprint10Agent


class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeFlaskBackEndSprint9Agent: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeFlaskBackEndSprint9Agent(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

    session_id_CodeFlaskBackEndSprint10Agent = "teste_handoff_CodeFlaskBackEndSprint10Agent"
    agent_, handoff_obj_CodeFlaskBackEndSprint10Agent = CodeFlaskBackEndSprint10Agent(session_id_CodeFlaskBackEndSprint10Agent, appcompany)

    createcheckout = '''
```python
@app.route('/api/create-checkout', methods=['POST'])
@limiter.limit("10 per minute")
def create_checkout():
    data = request.get_json()
    try:
        # Calcula a data de expiração: data atual + 31 dias
        expiration_time = datetime.now() + timedelta(days=31)

        checkout_session = stripe.checkout.Session.create(
            line_items=[{
                "price": SUBSCRIPTION_PRICE_ID,  # Usando o ID do preço definido no .env
                "quantity": 1
            }],
            mode="subscription",  # Modo de assinatura
            payment_method_types=["card"],
            success_url=f"{API_BASE_URL}/checkout/sucess",  
            cancel_url=f"{API_BASE_URL}/checkout/cancel",  
            metadata={
                "email": data.get("email"),
                "password": data.get("password"),
                "SUBSCRIPTION_PLAN": "premium",
                "TIMESTAMP": expiration_time.isoformat()
            },
        )
        logger.info("Sessão criada: %s", checkout_session.id)
        return jsonify({"sessionId": checkout_session.id})
    except Exception as e:
        logger.info("Erro ao criar a sessão de checkout: %s", str(e))
        return jsonify({"error": str(e)}), 500
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
        handoffs=[handoff_obj_CodeFlaskBackEndSprint10Agent],



    )


    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj