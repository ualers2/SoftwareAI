from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel

from modules.modules import *
from modules.Egetoolsv2 import *
from modules.EgetMetadataAgent import *


class Data(BaseModel):
    Content: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: Data):
    print(f"CodeBackendEndpointscodereviewAgent: {input_data.Content}")

def CodeBackendEndpointscodereviewAgent(session_id, appcompany):
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

   
    index_ = '''
# Rota para a landing page
@app.route('/')
def index():
    return render_template('index.html')
    '''
   
    login = '''
# Rota para a página de Login
@app.route('/login')
def login():
    return render_template('loginAndRegistrer.html')
    '''
   
    dashboard = '''
# Rota para a página de dashboard
@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')
    '''
   
    checkout = '''
# Rota para a página de Checkout de um plano específico
@app.route('/checkout')
def checkout():
    plan_name = request.args.get('plan', 'free')  # Valor padrão 'free'
    return render_template('checkout.html', plan=plan_name)
    '''
   
    checkout_sucess = '''
# Rota para exibir uma página de sucesso após o checkout
@app.route('/checkout/sucess')
def checkout_sucess():
    return render_template('success.html')

    '''
   
    api_create_checkout = '''
    
###############################################
# Endpoint de criação de Checkout (/api/create-checkout)
###############################################

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

    '''

   
    api_register = '''

###############################################
# Endpoint de Registro de Usuário (/api/register)
###############################################

@app.route('/api/register', methods=['POST'])
@limiter.limit("10 per minute")
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
    ref = db.reference(f'users/{email_safe}', app=app_instance)

    if ref.get():
        if not WEBHOOK_SECRET_flag:
            return jsonify({"error": "Voce ja tem uma conta"}), 400

        if WEBHOOK_SECRET_flag == WEBHOOK_SECRET:
            api_key = generate_api_key(SUBSCRIPTION_PLAN)
            ref.update({
                "api_key": api_key,
                "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
                "limit": limit,
                "expiration": expiration
            })
            return jsonify({
                "message": "Upgrade realizado",
                "email": email,
                "password": password,
                "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
                "limit": limit,
                "expiration": expiration,
                "api_key": api_key
            }), 409

    api_key = generate_api_key(SUBSCRIPTION_PLAN)
    ref.set({
        "email": email,
        "password": password,
        "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
        "limit": limit,
        "expiration": expiration,
        "api_key": api_key,
        "created_at": datetime.now().isoformat()
    })
    return jsonify({
        "message": "Usuário registrado com sucesso",
        "email": email,
        "password": password,
        "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
        "limit": limit,
        "expiration": expiration,
        "api_key": api_key,
        "created_at": datetime.now().isoformat()
    }), 200

    '''

   
    api_login = '''

###############################################
# Endpoint de Login (/api/login)
###############################################

@app.route('/api/login', methods=['POST'])
def apilogin():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email e senha são obrigatórios"}), 400

    email_safe = email.replace('.', '_')
    user = db.reference(f'users/{email_safe}', app=app_instance).get()

    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 404

    if user.get("password") != password:
        return jsonify({"error": "Senha incorreta"}), 401

    session['user'] = email
    session.permanent = True  # <- IMPORTANTE

    return jsonify({"message": "Login realizado com sucesso"}), 200

    '''

   
    webhook = '''

###############################################
# Endpoint do Webhook (/webhook)
###############################################

@app.route("/webhook", methods=["POST"])
@limiter.limit("10 per minute")
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
        return jsonify({"message": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        logger.info("Assinatura inválida")
        return jsonify({"message": "Invalid signature"}), 400

    # Processa o evento conforme o seu tipo 
    if event["type"] == "checkout.session.completed":
        session_data = event["data"]["object"]
        if session_data.get("payment_status") == "paid":
            email = session_data["metadata"].get("email")
            password = session_data["metadata"].get("password")
            SUBSCRIPTION_PLAN = session_data["metadata"].get("SUBSCRIPTION_PLAN")
            TIMESTAMP = session_data["metadata"].get("TIMESTAMP")
            logger.info("Pagamento por cartão com sucesso: %s, %s", email, SUBSCRIPTION_PLAN)

            data = {
                "email": email,
                "password": password,
                "WEBHOOK_SECRET_flag": WEBHOOK_SECRET,
                "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
                "expiration": TIMESTAMP,
            }
            headers = {
                "Content-Type": "application/json",
                "X-API-KEY": os.getenv("ADMIN_API_KEY", "default_api_key")
            }
            API_BASE_URL = os.getenv("API_BASE_URL")
            response = requests.post(f"{API_BASE_URL}/api/register", json=data, headers=headers)

            if response.status_code == 200:
                response_data = response.json()
                message = response_data.get("message")
                login_val = response_data.get("email")
                password_val = response_data.get("password")
                expiration = response_data.get("expiration")
                subscription_plan = response_data.get("SUBSCRIPTION_PLAN")
                api_key = response_data.get("api_key")

                logger.info(f"Mensagem: {message}")
                logger.info(f"Login: {login_val}")
                logger.info(f"Senha: {password_val}")
                logger.info(f"Expiração: {expiration}")
                logger.info(f"Plano de assinatura: {subscription_plan}")

                # Cria e envia o e-mail
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                import smtplib

                msg = MIMEMultipart()
                msg["From"] = gmail_usuario
                msg["To"] = email
                msg["Subject"] = "SoftwareAI"

                corpo = f"""
😀 Hello Here is your login, Thank you for choosing SoftwareAI

📱 Support Groups:
✨Discord:
✨Telegram:

💼 Chat Panel:
📌Login: {login_val}
📌Password: {password_val}

💼 Info Account:
📌api key: {api_key}
📌Expiration: {expiration}
📌Subscription plan: {subscription_plan}
                """
                msg.attach(MIMEText(corpo, "plain"))

                try:
                    servidor = smtplib.SMTP("smtp.gmail.com", 587)
                    servidor.starttls()
                    servidor.login(gmail_usuario, gmail_senha)
                    servidor.sendmail(gmail_usuario, email, msg.as_string())
                    servidor.quit()
                    logger.info("E-mail enviado com sucesso!")
                except Exception as e:
                    logger.info(f"Erro ao enviar e-mail: {e}")

            elif response.status_code == 409:
                logger.info("Parece que o usuario ja tem uma conta e possivelmente esta tentando atualizar para o premium")
                response_data = response.json()

                message = response_data.get("message")
                login_val = response_data.get("email")
                password_val = response_data.get("password")
                expiration = response_data.get("expiration")
                subscription_plan = response_data.get("SUBSCRIPTION_PLAN")
                api_key = response_data.get("api_key")

                logger.info(f"Mensagem: {message}")
                logger.info(f"Login: {login_val}")
                logger.info(f"Senha: {password_val}")
                logger.info(f"Expiração: {expiration}")
                logger.info(f"Plano de assinatura: {subscription_plan}")

                # Cria e envia o e-mail de upgrade
                from email.mime.multipart import MIMEMultipart
                from email.mime.text import MIMEText
                import smtplib

                msg = MIMEMultipart()
                msg["From"] = gmail_usuario
                msg["To"] = email
                msg["Subject"] = "SoftwareAI"

                corpo = f"""
😀 Hi, Your account has been upgraded. Thank you for choosing and trusting SoftwareAI

📱 Support Groups:
✨Discord:
✨Telegram:

💼 Chat Panel:
📌Login: {login_val}
📌Password: {password_val}

💼 Account Information:
📌API Key: {api_key}
📌Expiration: {expiration}
📌Subscription Plan: {subscription_plan}
                """
                msg.attach(MIMEText(corpo, "plain"))

                try:
                    servidor = smtplib.SMTP("smtp.gmail.com", 587)
                    servidor.starttls()
                    servidor.login(gmail_usuario, gmail_senha)
                    servidor.sendmail(gmail_usuario, email, msg.as_string())
                    servidor.quit()
                    logger.info("E-mail enviado com sucesso!")
                except Exception as e:
                    logger.info(f"Erro ao enviar e-mail: {e}")

        elif session_data.get("payment_status") == "unpaid" and session_data.get("payment_intent"):
            payment_intent = stripe.PaymentIntent.retrieve(session_data["payment_intent"])
            hosted_voucher_url = (payment_intent.next_action and payment_intent.next_action.get("boleto_display_details", {}).get("hosted_voucher_url"))
            if hosted_voucher_url:
                user_email = session_data.get("customer_details", {}).get("email")
                logger.info("Gerou o boleto e o link é %s", hosted_voucher_url)

    elif event["type"] == "checkout.session.expired":
        session_data = event["data"]["object"]
        if session_data.get("payment_status") == "unpaid":
            teste_id = session_data["metadata"].get("testeId")
            logger.info("Checkout expirado %s", teste_id)

    elif event["type"] == "checkout.session.async_payment_succeeded":
        session_data = event["data"]["object"]
        if session_data.get("payment_status") == "paid":
            teste_id = session_data["metadata"].get("testeId")
            logger.info("Pagamento boleto confirmado %s", teste_id)

    elif event["type"] == "checkout.session.async_payment_failed":
        session_data = event["data"]["object"]
        if session_data.get("payment_status") == "unpaid":
            teste_id = session_data["metadata"].get("testeId")
            logger.info("Pagamento boleto falhou %s", teste_id)

    elif event["type"] == "customer.subscription.deleted":
        logger.info("Cliente cancelou o plano")

    return jsonify({"result": event, "ok": True})

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
        tools=Tools_Name_dict
    )

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=Data,
    )
    return agent, handoff_obj