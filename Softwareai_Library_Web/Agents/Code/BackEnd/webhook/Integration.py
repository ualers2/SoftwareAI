from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *

# from Agents.Code.BackEnd.Sprint11.Integration import CodeFlaskBackEndSprint11Agent

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeFlaskBackEndSprint10Agent: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeFlaskBackEndSprint10Agent(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

    # session_id_CodeFlaskBackEndSprint11Agent = "teste_handoff_CodeFlaskBackEndSprint11Agent"
    # agent_, handoff_obj_CodeFlaskBackEndSprint11Agent = CodeFlaskBackEndSprint11Agent(session_id_CodeFlaskBackEndSprint11Agent, appcompany)

   
    code_webhook = '''
```python
@app.route("/webhook", methods=["POST"])
def stripe_webhook():
    """
    Endpoint para tratar os webhooks enviados pela Stripe.
    """
    payload = request.data
    sig_header = request.headers.get("Stripe-Signature")
    event = None

    try:
        event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
    except ValueError as e:
        logger.info("Payload inválido")
        return jsonify({{"message": "Invalid payload"}}), 400
    except stripe.error.SignatureVerificationError as e:
        logger.info("Assinatura inválida")
        return jsonify({{"message": "Invalid signature"}}), 400

    # Processa o evento conforme o seu tipo
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            email = session["metadata"].get("email")
            password = session["metadata"].get("password")
            SUBSCRIPTION_PLAN = session["metadata"].get("SUBSCRIPTION_PLAN")
            TIMESTAMP = session["metadata"].get("TIMESTAMP")
            logger.info("Pagamento por cartão com sucesso", email, SUBSCRIPTION_PLAN)

            data = {
                "email": email,
                "password": password,
                "WEBHOOK_SECRET_flag": WEBHOOK_SECRET,
                "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
                "expiration": TIMESTAMP,
                
            }
            headers = {
                    "Content-Type": "application/json",
                    "X-API-KEY": ADMIN_API_KEY
                    }
            response = requests.post("{API_BASE_URL}/api/register", json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                
                # Obtém cada argumento retornado pelo endpoint
                message = response_data.get("message")
                login = response_data.get("email")
                password = response_data.get("password")
                expiration = response_data.get("expiration")
                subscription_plan = response_data.get("SUBSCRIPTION_PLAN")
                api_key = response_data.get("api_key")
                
                # Exibe os valores obtidos
                logger.info(f"Mensagem: {message}")
                logger.info(f"Login: {login}")
                logger.info(f"Senha: {password}")
                logger.info(f"Expiração: {expiration}")
                logger.info(f"Plano de assinatura: {subscription_plan}")

                # Criar a mensagem
                msg = MIMEMultipart()
                msg["From"] = gmail_usuario
                msg["To"] = email
                msg["Subject"] = "SoftwareAI"

                # Corpo do e-mail
                corpo = f"""
😀 Hello Here is your login, Thank you for choosing SoftwareAI

📱 Support Groups
✨Discord: 
✨Telegram: 

💼 Chat Panel:
📌Login:
{login}
📌Password:
{password}

💼 Info Account:
📌api key:
{api_key}
📌Expiration:
{expiration}
📌Subscription plan:
{subscription_plan}


                """
                msg.attach(MIMEText(corpo, "plain"))

                try:
                    # Conectar ao servidor SMTP do Gmail
                    servidor = smtplib.SMTP("smtp.gmail.com", 587)
                    servidor.starttls()  # Segurança
                    servidor.login(gmail_usuario, gmail_senha)  # Autenticação
                    servidor.sendmail(gmail_usuario, email, msg.as_string())  # Enviar e-mail
                    servidor.quit()

                    logger.info("E-mail enviado com sucesso!")

                except Exception as e:
                    logger.info(f"Erro ao enviar e-mail: {e}")

            elif response.status_code == 409:
                logger.info("Parece que o usuario ja tem uma conta e possivelmente esta tentando atualizar para o premium")
                response_data = response.json()
                
                # Obtém cada argumento retornado pelo endpoint
                message = response_data.get("message")
                login = response_data.get("email")
                password = response_data.get("password")
                expiration = response_data.get("expiration")
                subscription_plan = response_data.get("SUBSCRIPTION_PLAN")
                api_key = response_data.get("api_key")
                
                # Exibe os valores obtidos
                logger.info(f"Mensagem: {message}")
                logger.info(f"Login: {login}")
                logger.info(f"Senha: {password}")
                logger.info(f"Expiração: {expiration}")
                logger.info(f"Plano de assinatura: {subscription_plan}")

                # Criar a mensagem
                msg = MIMEMultipart()
                msg["From"] = gmail_usuario
                msg["To"] = email
                msg["Subject"] = "SoftwareAI"

                # Corpo do e-mail
                corpo = f"""
😀 Hi, Your account has been upgraded. Thank you for choosing and trusting SoftwareAI
📱 Support Groups
✨Discord: 
✨Telegram: 

💼 Chat Panel:
📌Login:
{login}
📌Password:
{password}

💼 Account Information:
📌API Key:
{api_key}
📌Expiration:
{expiration}
📌Subscription Plan:
{subscription_plan}

                """
                msg.attach(MIMEText(corpo, "plain"))

                try:
                    # Conectar ao servidor SMTP do Gmail
                    servidor = smtplib.SMTP("smtp.gmail.com", 587)
                    servidor.starttls()  # Segurança
                    servidor.login(gmail_usuario, gmail_senha)  # Autenticação
                    servidor.sendmail(gmail_usuario, email, msg.as_string())  # Enviar e-mail
                    servidor.quit()

                    logger.info("E-mail enviado com sucesso!")

                except Exception as e:
                    logger.info(f"Erro ao enviar e-mail: {e}")

        elif session.get("payment_status") == "unpaid" and session.get("payment_intent"):
            payment_intent = stripe.PaymentIntent.retrieve(session["payment_intent"])
            hosted_voucher_url = (
                payment_intent.next_action
                and payment_intent.next_action.get("boleto_display_details", {})
                .get("hosted_voucher_url")
            )
            if hosted_voucher_url:
                user_email = session.get("customer_details", {}).get("email")
                logger.info("Gerou o boleto e o link é", hosted_voucher_url)
    
    elif event["type"] == "checkout.session.expired":
        session = event["data"]["object"]
        if session.get("payment_status") == "unpaid":
            teste_id = session["metadata"].get("testeId")
            logger.info("Checkout expirado", teste_id)
    
    elif event["type"] == "checkout.session.async_payment_succeeded":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            teste_id = session["metadata"].get("testeId")
            logger.info("Pagamento boleto confirmado", teste_id)
    
    elif event["type"] == "checkout.session.async_payment_failed":
        session = event["data"]["object"]
        if session.get("payment_status") == "unpaid":
            teste_id = session["metadata"].get("testeId")
            logger.info("Pagamento boleto falhou", teste_id)
    
    elif event["type"] == "customer.subscription.deleted":
        logger.info("Cliente cancelou o plano")
    
    return jsonify({"result": event, "ok": True})
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
        # handoffs=[handoff_obj_CodeFlaskBackEndSprint11Agent],


    )


    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj