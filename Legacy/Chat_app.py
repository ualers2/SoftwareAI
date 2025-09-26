
# IMPORT SoftwareAI Libs
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
from softwareai_engine_library.Chat._init_chat_ import *
#########################################
from softwareai_engine_library.EngineProcess.EgetMetadataAgent import *
#########################################
from softwareai_engine_library.EngineProcess.EgetTools import *
#########################################
# from AgentsWorkFlow.Saas.Code.BackEnd.api_create_checkout.Integration import CodeFlaskBackEndapi_create_checkoutAgent
# from AgentsWorkFlow.Saas.Code.BackEnd.api_login.Integration import CodeFlaskBackEndapi_loginAgent
# from AgentsWorkFlow.Saas.Code.BackEnd.api_register.Integration import CodeFlaskBackEndapi_registerAgent
# from AgentsWorkFlow.Saas.Code.BackEnd.basic_endpoints.Integration import CodeFlaskBackEnd_basic_endpointsAgent
# from AgentsWorkFlow.Saas.Code.BackEnd.webhook.Integration import CodeFlaskBackEndwebhookAgent

# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_BackEnd_Endpoints.Integration import CodeBackendEndpointscodereviewAgent
# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_DevOps_Docker.Integration import CodeReview_DevOps_Docker
# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_FrontEnd_Html.Integration import CodeReviewFrontEndHtmlAgent
# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_FrontEnd_JS.Integration import CodeReviewFrontEndJSAgent
# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_Keys.Integration import CodeReviewKeysAgent
# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_Preproject.Integration import CodeReview_Preproject
# from AgentsWorkFlow.Saas.Code.CodeReview.CodeReview_Timeline.Integration import CodeReview_Timeline

# from AgentsWorkFlow.Saas.Code.DevOps.DeployProjectModeEasy.Integration import DeployProjectModeEasy
# from AgentsWorkFlow.Saas.Code.DevOps.DockerBuild.Integration import CodeDockerBuildAgent
# from AgentsWorkFlow.Saas.Code.DevOps.DockerCompose.Integration import CodeDockerComposeAgent
# from AgentsWorkFlow.Saas.Code.DevOps.DockerFile.Integration import CodeDockerFileAgent
# from AgentsWorkFlow.Saas.Code.DevOps.GitUpload.Integration import CodeUploadGit
# from AgentsWorkFlow.Saas.Code.DevOps.RequirementsTxt.Integration import CodeRequirementstxtAgent
# from AgentsWorkFlow.Saas.Code.DevOps.RunBuildProject.Integration import RunBuildProject

# from AgentsWorkFlow.Saas.Code.FrontEnd.Checkout.Integration import CodeCheckoutFrontEnd
# from AgentsWorkFlow.Saas.Code.FrontEnd.Index.Integration import CodeIndexFrontEnd
# from AgentsWorkFlow.Saas.Code.FrontEnd.Login.Integration import CodeLoginFrontEnd
# from AgentsWorkFlow.Saas.Code.FrontEnd.NavigationJS.Integration import CodeNavigationJSFrontEnd

# from AgentsWorkFlow.Saas.Code.ProductManager.CreateProduct.Integration import CreateProduct

# from AgentsWorkFlow.Saas.Code.ProjectManager.Documentation.Modules.Integration import CodeDocumentationModulesAgent
# from AgentsWorkFlow.Saas.Code.ProjectManager.Documentation.Staticjs.Integration import CodeDocumentationStaticjsAgent
# from AgentsWorkFlow.Saas.Code.ProjectManager.Documentation.Technich.Integration import CodeDocumentationTechnichAgent
# from AgentsWorkFlow.Saas.Code.ProjectManager.Keys_env.Integration import CodeFlaskBackEndKeysenvAgent
# from AgentsWorkFlow.Saas.Code.ProjectManager.Keys_fb.Integration import CodeFlaskBackEnd_Keys_fb_STATIC
# from AgentsWorkFlow.Saas.Code.ProjectManager.Timeline.Integration import CodeRequirementsAndTimeline

# from AgentsWorkFlow.Saas.Code.QA.unittest_login_user_by_ui.Integration import unittest_login_user_by_ui
# from AgentsWorkFlow.Saas.Code.QA.unittest_user_checkout_by_ui.Integration import unittest_user_checkout_by_ui
# from AgentsWorkFlow.Saas.Code.QA.unittest_user_created_by_ui.Integration import unittest_user_created_by_ui

# from AgentsWorkFlow.Saas.Decisions.Dashboard_Decision.Integration import CodeFrontEndDecisionDashboard
# from AgentsWorkFlow.Saas.Decisions.TypeProject.Integration import TriageAgent


from Keys.keys import *

dotenv_path = os.path.join(os.path.dirname(__file__), "Keys", "keys.env")
load_dotenv(dotenv_path=dotenv_path)

# from Decisions.TypeProject.triage_agent import TriageAgent


os.chdir(os.path.join(os.path.dirname(__file__)))

# Habilita modo inseguro para OAuth (útil para dev local)
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

load_dotenv(dotenv_path="Keys/keys.env", override=True)


API_BASE_URL = os.getenv("API_BASE_URL")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GITHUB_CLIENT_ID = os.getenv("GITHUB_CLIENT_ID")
GITHUB_CLIENT_SECRET = os.getenv("GITHUB_CLIENT_SECRET")
GITHUB_REDIRECT_URI = os.getenv("GITHUB_REDIRECT_URI") 
AGENTS_DIR = os.getenv("AGENTS_DIR")  
path_relatorio =  os.getenv("path_relatorio")  
createlogin = os.getenv("createlogin")
gmail_usuario = os.getenv("gmail_usuario")
gmail_senha = os.getenv("gmail_senha")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
PRICE_ID = os.getenv("STRIPE_PRICE_ID")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
ADMIN_API_KEY =  os.getenv("ADMIN_API_KEY")
key_openai = os.getenv("OPENAI_API_KEY")



client = OpenAI(api_key=key_openai)
appcompany = init_firebase_appcompany()

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, supports_credentials=True, origins="*")

app.secret_key = 'sua_chave_secreta' 
app.permanent_session_lifetime = timedelta(days=7)  # exemplo: sessão dura 7 dias
app.config['SESSION_COOKIE_SECURE'] = False  # necessário em localhost
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # ou 'None' se for domínio cruzado

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

# 📌 Bloqueia spam (aplica limites apenas para tentativas inválidas)
limiter = Limiter(
    app=app,
    key_func=key_func,
    default_limits=["10 per minute"]
)

limit = "10 per minute"

@app.context_processor
def inject_static_url():
    return dict(static_url=url_for('static', filename=''))

@app.route('/')
def index():
    logger.info(f"WEBHOOK_SECRET{WEBHOOK_SECRET}")
    return render_template('home.html')

@app.route('/chat')
@login_required
def chat():
    if 'user' not in session:
        return redirect(url_for('login')) 
    return render_template('chat.html')

@app.route('/dashboard')
@login_required
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login')) 
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/plan/prolight/checkout')
def plan_premium_checkout():
    return render_template('checkout/checkout.html')
 
@app.route('/checkout/sucess')
def checkoutsucess():
    return render_template('checkout/success.html')

@app.route('/checkout/cancel')
def checkoutcancel():
    return render_template('checkout/cancel.html')

@app.route('/api/me')
def get_current_user():
    if 'user' not in session:
        return jsonify({"logged_in": False}), 401
    return jsonify({
        "logged_in": True,
        "email": session["user"]
    })

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
        limit = "20 per day"
        agents = "1"
        projects_per_day = "1"
    elif SUBSCRIPTION_PLAN == "premium":
        limit = "100 per day"
        agents = "40"
        projects_per_day = "5"

    email_safe = email.replace('.', '_')
    ref = db.reference(f'users/{email_safe}', app=appcompany)
    ref_settings = db.reference(f'users/{email_safe}/settings/dashboard', app=appcompany)
    ref_settings_github = db.reference(f'users/{email_safe}/settings/github', app=appcompany)
    ref_settings_firebase_config = db.reference(f'users/{email_safe}/settings/firebase_config', app=appcompany)
    ref_conversations = db.reference(f'users/{email_safe}/conversations', app=appcompany)

    

    if ref.get():
        if not WEBHOOK_SECRET_flag:
            return jsonify({"error": "Voce ja tem uma conta com esse email"}), 400
        
        if WEBHOOK_SECRET_flag == WEBHOOK_SECRET:
                
            api_key = generate_api_key(SUBSCRIPTION_PLAN)

            ref.update({
                "api_key": api_key,
                "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
                "limit": limit,
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

    payload = {
        "agents": agents,
        "projects_per_day": projects_per_day,
        "email": email,
        "password": password,
        "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
        "limit": limit,
        "expiration": expiration,
        "api_key": api_key,
        'created_at': datetime.now().isoformat()
    }
    payload_settings = {
        "agentWorkMode": "None",
        "githubCompany": "None",
        "githubTypeProject": "None",
        "gmail_usuario": "None",
        "gmail_senha": "None",
        "sciaAlgorithm": "None",
        "sciamode": "None",
        "stripePublicKey": "None",
        "stripeSecretKey": "None",
        "selectedAgents": "None",
        "githubRepositories": "None"
    }
    payload_github = {
        "github_access_token": "None",
        "github_username": "None",
    }
    # payload_firebase_config = {
    #     "firebase_config": "None",
    # }
    payload_conversations = {
        "conversations": "None",
    }

    
    ref.set(payload)
    ref_settings.set(payload_settings)
    ref_settings_github.set(payload_github)
    # ref_settings_firebase_config.set(payload_firebase_config)
    ref_conversations.set(payload_conversations)

    
    return jsonify({
        "message": "Usuário registrado com sucesso",
        }), 200


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


@app.route("/api/create-stripe-onboarding-link", methods=["POST"])
def create_stripe_onboarding_link():
    try:
        email = request.json.get("email")
        if not email:
            return jsonify({"error": "Email é obrigatório"}), 400

        # Normaliza o email
        email_safe = email.replace('.', '_')

        # Referência do usuário no DB
        ref = db.reference(f'users/{email_safe}/settings', app=appcompany)

        # Verifica se usuário existe
        user_data = ref.get()
        if not user_data:
            return jsonify({"error": "Usuário não encontrado"}), 404

        # Cria conta Stripe conectada
        account = stripe.Account.create(
            type="express"
        )

        # Atualiza usuário no Firebase com o ID da conta Stripe
        ref.update({
            "stripe_account_id": account.id
        })

        # Cria o link de onboarding
        account_link = stripe.AccountLink.create(
            account=account.id,
            refresh_url="https://seusite.com/erro",
            return_url="https://seusite.com/sucesso",
            type="account_onboarding"
        )

        return jsonify({"url": account_link.url})

    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route("/api/stripe-connection-status", methods=["POST"])
def stripe_connection_status():
    try:
        email = request.json.get("email")
        if not email:
            return jsonify({"error": "Email é obrigatório"}), 400

        email_safe = email.replace('.', '_')
        ref = db.reference(f'users/{email_safe}/settings', app=appcompany)
        user_data = ref.get()

        if not user_data:
            return jsonify({"error": "Usuário não encontrado"}), 404

        has_stripe = "stripe_account_id" in user_data and user_data["stripe_account_id"] != ""

        return jsonify({
            "connected": has_stripe,
            "stripe_account_id": user_data.get("stripe_account_id", None)
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/api/reset-firebase-config", methods=["POST"])
def reset_firebase_config():
    data = request.get_json()
    email = data.get("email")
    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    email_safe = email.replace('.', '_')

    # Referência direta ao campo firebase_config
    ref = db.reference(f'users/{email_safe}/settings/firebase_config', app=appcompany)
    ref.delete()

    return jsonify({"status": "reset_success"})

@app.route("/api/check-firebase-config", methods=["GET"])
def check_firebase_config():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    email_safe = re.sub(r"[.]", "_", email)
    ref = db.reference(f'users/{email_safe}/settings/firebase_config', app=appcompany)
    config_data = ref.get()

    return jsonify({
        "status": "connected" if config_data else "disconnected"
    })

@app.route("/api/save-firebase-config", methods=["POST"])
def save_firebase_config():
    data = request.json
    email = data.get("email")  # frontend deve enviar junto!
    config = data.get("config")

    if not email or not config:
        return jsonify({"error": "Faltando email ou config"}), 400

    email_safe = email.replace('.', '_')
    ref = db.reference(f'users/{email_safe}/settings/firebase_config', app=appcompany)
    ref.set(config)

    return jsonify({"status": "salvo"})

@app.route("/api/load-firebase-config")
def load_firebase_config():
    email = request.args.get("email")
    if not email:
        return jsonify({"error": "Email ausente"}), 400

    email_safe = email.replace('.', '_')
    ref = db.reference(f'users/{email_safe}/settings/firebase_config', app=appcompany)
    config = ref.get()

    if not config:
        return jsonify({"error": "Config não encontrada"}), 404

    return jsonify(config)
    

@app.route("/login/github")
def login_github():
    # Gere um novo state token para segurança
    state = secrets.token_hex(16)
    session['github_oauth_state'] = state
    
    # Construa a URL de autorização manualmente
    github_auth_url = f"https://github.com/login/oauth/authorize?client_id={GITHUB_CLIENT_ID}&redirect_uri={GITHUB_REDIRECT_URI}&state={state}&"
    scopes = "repo read:org user:email"
    github_auth_url = (
        "https://github.com/login/oauth/authorize"
        f"?client_id={GITHUB_CLIENT_ID}"
        f"&redirect_uri={GITHUB_REDIRECT_URI}"
        f"&state={state}"
        f"&scope={urllib.parse.quote(scopes)}"
        f"&prompt=consent"

    )
    return redirect(github_auth_url)

@app.route("/callback/github")
def github_callback():
    # Verifique o state para segurança contra CSRF
    if 'github_oauth_state' not in session or request.args.get('state') != session['github_oauth_state']:
        return redirect(url_for('index'))
    
    session.pop('github_oauth_state', None)  # Limpa o state

    code = request.args.get('code')
    if not code:
        return redirect(url_for('index'))

    # Troca código por token
    token_url = "https://github.com/login/oauth/access_token"
    payload = {
        "client_id": GITHUB_CLIENT_ID,
        "client_secret": GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": GITHUB_REDIRECT_URI
    }
    headers = {"Accept": "application/json"}

    try:
        token_response = requests.post(token_url, data=payload, headers=headers)
        token_data = token_response.json()

        if 'access_token' not in token_data:
            logger.info(f"Erro ao obter token: {token_data.get('error_description', 'Desconhecido')}")
            return redirect(url_for('index'))

        access_token = token_data['access_token']

        # Busca dados do usuário
        user_url = "https://api.github.com/user"
        user_headers = {
            "Authorization": f"token {access_token}",
            "Accept": "application/json"
        }

        user_response = requests.get(user_url, headers=user_headers)
        github_data = user_response.json()

        github_username = github_data.get("login")
        github_id = github_data.get("id")

        # 🟢 Pega o usuário atual da sessão
        user_email = session.get("user")
        if not user_email:
            logger.info("Sessão sem e-mail")
            return redirect(url_for('index'))

        user_key = user_email.replace(".", "_")

        # 🔥 Salva os dados no perfil do usuário
        db.reference(f"users/{user_key}/settings/github", app=appcompany).update({
            "github_access_token": access_token,
            "github_username": github_username
        })

        # Atualiza a sessão (opcional, só se quiser)
        session['github_user'] = github_username
        session['github_access_token'] = access_token
        session['github_authenticated'] = True

        return redirect('/dashboard')

    except Exception as e:
        logger.info(f"Erro durante autenticação GitHub: {str(e)}")
        return redirect(url_for('index'))

@app.route("/logout/github")
def logout_github():
    session.pop('github_authenticated', None)
    session.pop('github_user', None)
    return redirect(url_for('index'))

@app.route('/api/github/reset', methods=['POST'])
def reset_github_config():
    if 'user' not in session:
        return jsonify({"error": "Not authenticated"}), 401

    user_email = session['user']
    user_key = user_email.replace(".", "_")
    user_ref = db.reference(f'users/{user_key}/settings/github', app=appcompany)

    # Remove o token salvo no Firebase
    user_ref.update({"github_access_token": None})
    user_ref.update({"github_username": None})

    # Limpa também da sessão
    session.pop('githubToken', None)

    return jsonify({"message": "GitHub configuration reset successfully."})

@app.route("/api/github/firebase-status/<int:github_id>")
def github_firebase_status(github_id):
    ref = db.reference(f"sessions/github/{github_id}/firebase_config")
    data = ref.get()

    if not data:
        return jsonify({"connected": False})

    if int(time.time()) > data["expires_at"]:
        return jsonify({"connected": False, "reason": "expired"})

    return jsonify({
        "connected": True,
        "username": data["username"]
    })

@app.route("/api/github/status", methods=["GET"])
def github_status():
    logger.info("Sessão atual em /api/github/status:", dict(session))

    if "user" not in session:
        return jsonify({"connected": False})

    user_email = session["user"]
    email_safe = user_email.replace(".", "_")
    user_data_github = db.reference(f'users/{email_safe}/settings/github', app=appcompany).get()
    user_data_settings = db.reference(f'users/{email_safe}/settings', app=appcompany).get()

    # logger.info(f"Dados do usuário em settings:{agent_settings_data}")

    github_token = user_data_github.get("github_access_token")
    github_username = user_data_github.get("github_username", "unknown")
    githubRepositories = user_data_settings.get("githubRepositories")
    selectedAgents = user_data_settings.get("selectedAgents")

    if not github_token:
        return jsonify({"connected": False})

    # Verifica se o token está válido acessando a API do GitHub
    headers = {
        "Authorization": f"Bearer {github_token}",
        "Accept": "application/vnd.github+json"
    }

    try:
        test_response = requests.get("https://api.github.com/user/repos?per_page=1", headers=headers, timeout=5)
        if test_response.status_code != 200:
            logger.warning(f"Token GitHub expirado ou inválido: {test_response.text}")
            return jsonify({"connected": False})
    except Exception as e:
        logger.exception("Erro ao verificar token GitHub:")
        return jsonify({"connected": False})

    return jsonify({
        "connected": True,
        "username": github_username,
        "access_token": github_token,
        "githubRepositories": githubRepositories,
        "selectedAgents": selectedAgents,
    })


@app.route('/api/release/deploy', methods=['POST'])
def deploy_to_release():
    data = request.get_json()
    github_repo_url = data.get("repo_url")
    github_token = session.get("githubToken")
    release_token = session.get("releaseToken")  # Vamos armazenar isso ao conectar

    if not all([github_repo_url, github_token, release_token]):
        return jsonify({"error": "Missing required data"}), 400

    headers = {
        "Authorization": f"Bearer {release_token}",
        "Content-Type": "application/json"
    }

    payload = {
        "source": {
            "provider": "github",
            "repo_url": github_repo_url,
            "branch": "main"
        }
    }

    release_api = "https://api.release.com/v1/environments"
    response = requests.post(release_api, headers=headers, json=payload)

    if response.status_code == 201:
        env_url = response.json().get("environment", {}).get("url", "Link não retornado")
        return jsonify({"success": True, "url": env_url})
    else:
        return jsonify({"error": response.text}), response.status_code

@app.route('/api/connect-release', methods=['POST'])
def connect_release():
    data = request.get_json()
    release_token = data.get("release_token")
    user_email = session["user"]

    # Salva no Firebase
    db.reference(f'users/{user_email.replace(".", "_")}', app=appcompany).update({
        "release_token": release_token
    })

    # Armazena na sessão
    session["releaseToken"] = release_token

    return jsonify({"success": True})



@app.route('/api/response-conversation/documentation-architect-agent', methods=['POST'])
@limiter.limit(lambda: dynamic_rate_limit(appcompany))
def chat_codepreproject():
    message = request.form.get("message")
    session_id = request.form.get("session_id")
    user_email = request.form.get("user_email")
    images = request.files.getlist("images")
    files = request.files.getlist("files")

    usuario, erro = autenticar_usuario(appcompany=appcompany)
    if erro:
        return erro
    
    api_key = get_api_key()
    if not api_key:
        return jsonify({"error": "API Key não fornecida."}), 401

    url = "https://code-preproject.rshare.io/api/CodePreProject/NewProject"
    payload = {
        "data": {
            "mensagem": message,
        }
    }
    #crie uma landing page para meu saas de agente de ia que realiza code refact em grandes bases de codigo"
   
    response = requests.post(url, json=payload)
    payload = response.json()
    status = payload["status"]
    response = payload["response"]
    doc_md_content = payload["doc_md_content"]

    return jsonify({
        "status": status,
        "response": response,
        "doc_md_content": doc_md_content
    }), 201



# @app.route('/api/response-conversation', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))
# def api_response_conversation():
#     message = request.form.get("message")
#     session_id = request.form.get("session_id")
#     user_email = request.form.get("user_email")
#     images = request.files.getlist("images")
#     files = request.files.getlist("files")

#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro
    

#     # SUPPORTED_MIME_TYPES = {
#     #     ".c": "text/x-c",
#     #     ".cpp": "text/x-c++",
#     #     ".cs": "text/x-csharp",
#     #     ".css": "text/css",
#     #     ".doc": "application/msword",
#     #     ".docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#     #     ".go": "text/x-golang",
#     #     ".html": "text/html",
#     #     ".java": "text/x-java",
#     #     ".js": "text/javascript",
#     #     ".json": "application/json",
#     #     ".md": "text/markdown",
#     #     ".pdf": "application/pdf",
#     #     ".php": "text/x-php",
#     #     ".pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
#     #     ".py": "text/x-python",
#     #     ".rb": "text/x-ruby",
#     #     ".sh": "application/x-sh",
#     #     ".tex": "text/x-tex",
#     #     ".ts": "application/typescript",
#     #     ".txt": "text/plain"
#     # }

#     if not user_email:
#         return jsonify({"error": "user_email is required"}), 400
    
#     ref = db.reference(f'agent_settings/{user_email.replace(".", "_")}', app=appcompany)
#     data_user = ref.get()
#     companyname = data_user.get("githubCompany")

#     ref = db.reference(f'users/{user_email.replace(".", "_")}', app=appcompany)
#     data_user = ref.get()
#     github_token = data_user.get("github_token")

# #     instructions_general = f"""
# #     Meu nome é ChatManager, Sou um pensador que responde mensagens importantes e para isso utilizo cada ferramenta segundo as minhas regras 

# #     Regras:
# #     Regra 1 - Caso seja solicitado algum Pdf e Utilizo a ferramenta **autoPdf** para Criar o projeto 
# #     Apos criar o projeto Respondo no formato JSON Exemplo: {{
# #         'request_project': 'descricao detalhada da solicitacao',
# #         'nome_project: 'nome do projeto'
# #     }}

# #     Regra 2 - Caso seja solicitado algum relatorio em imagem eu Utilizo a ferramenta **criar_grafico** para Criar um grafico para o relatorio 
# #     Apos criar do grafico do relatorio Respondo no formato JSON Exemplo: {{
# #         'request_project': 'descricao detalhada da solicitacao',
# #         'relatorio_path: 'caminho pára o relatorio'
# #     }}

# #     ### **Detalhes do criar_grafico:**  
# #     - **tipo:** 'linha', 'barra' ou 'pizza'
# #     - **dados:** dados fornecidos pelo usuario
# #     - **titulo:** Título do gráfico.
# #     - **xlabel:** Rótulo do eixo X (para linha/barra).
# #     - **ylabel:** Rótulo do eixo Y (para linha/barra).
# #     - **salvar_em:** {path_relatorio}


# #     """

# #     instructions_general_assistant = f"""
# # Meu nome é Quantum, 
# # Sou um desenvolvedor que faz parte do time de desenvolvimento

# # ### **Missão:** 

# # Minha responsabilidade é Analisar e implementar as melhorias propostas pelo usuario


# # ### **Fluxo de Trabalho Automatizado:**  

# # 2. **Gerando o Código Completo:**  
# # - **html** Crie e salve (usando autosave) o código completo Para o html.  
# # - **Após a criação do html** utilize a ferramenta **send_to_webhook_func** para notificar via webhook sobre os detalhes do que foi implementado no html
# # ### **Regras Rígidas:**  
# # - **É obrigatório retornar o código completo e atualizado.**  
# # - **Nunca enviar apenas trechos de código ou mensagens incompletas.**  
# # - **Mantenha a estrutura e a lógica original do código.**  
# # - **Não envie respostas incompletas ou parciais**.  



# # 5. **Automatize o Pull Request:**  
# # - **Crie automaticamente**:  
# #     - Uma **Commit Message** clara e descritiva.  
# #     - Um **Título do Pull Request (PR)** direto e objetivo.  
# #     - Uma **Descrição detalhada** explicando as melhorias.  
# #     - Um **Branch Name** relacionado à principal melhoria.  
# # - Utilize a ferramenta **autopullrequest** para abrir o PR.
# # - Após a criação do PR, utilize a ferramenta **send_to_webhook_func** para notificar via chat sobre os detalhes do pr

# # # ### **Detalhes do autopullrequest:**  
# # # - **repo_owner:** {companyname}
# # # - **repo_name:** nome do repositorio
# # # - **branch_name:** nome curto para a branch do pull request
# # # - **file_paths:** a lista de caminhos para os arquivos a serem carregados no pull request 
# # # - **commit_message:** a mensagem com descrição do que foi melhorado com o pull request
# # # - **improvements:** a lista de conteudo completo para os arquivos a serem carregados no pull request 
# # # - **pr_title:** o titulo objetivo para o pr
# # # - **github_token:** {github_token}

# # # ### **Detalhes send_to_webhook_func:**  
# # # - **user:** CodeWebSite Agent
# # # - **type:** info
# # # - **message:** mensagem do usuario
# # # - **cor:** blue

# # # ### **Detalhes do autosave:**  
# # # - **code:** conteudo do arquivo
# # # - **path:** caminho do arquivo a ser salvo

# # ---

# # ### **Diretrizes para Geração Automática:**  

# # #### **Commit Message:**  
# # - **feat:** Para novas funcionalidades.  
# # - Exemplo: **feat:** Adiciona autenticação de usuário com OAuth 2.0.  
# # - **fix:** Para correções de bugs.  
# # - Exemplo: **fix:** Corrige erro na autenticação via API.  
# # - **refactor:** Para melhorias sem alteração de comportamento.  
# # - Exemplo: **refactor:** Refatora classes para melhorar a legibilidade.

# # #### **Título do PR:**  
# # - Deve ser direto e refletir a principal melhoria.  
# # - Exemplo: **Refatora autenticação de usuário**

# # #### **Descrição do PR:**  
# # - **Problema:** Explique o problema identificado.  
# # - **Solução:** Detalhe as melhorias implementadas.  
# # - **Impacto:** Informe como a mudança afeta o sistema.

# # #### **Branch Name:**  
# # - **feat/nome-da-funcionalidade**  
# # - **fix/correcao-do-bug**  
# # - **refactor/ajuste-no-codigo**  
# # - Exemplo: **fix/authentication-error**

# # ---


# #     """


# #     instructions_rules = f"""       
# #     """

# #     instructions_additional = ""

# #     instrucoes = f"{instructions_general}{instructions_rules}"

#     # # Salvar os dados binários das imagens em memória
#     # image_data_list = []
#     # if images:
#     #     for image in images:
#     #         ext = image.filename.split('.')[-1].lower()
#     #         mime_type = f"image/{ext if ext != 'jpg' else 'jpeg'}"
#     #         image_bytes = image.read()
#     #         encoded_image = base64.b64encode(image_bytes).decode("utf-8")
#     #         image_data_list.append({
#     #             "mime_type": mime_type,
#     #             "encoded_image": encoded_image
#     #         })

#     # # 🔼 Upload dos arquivos para a OpenAI com propósito 'assistants'
#     # uploaded_file_ids = []
#     # file_descriptions = []
#     # if files:
#     #     for file in files:
#     #         filename = file.filename
#     #         ext = os.path.splitext(filename)[-1].lower()
#     #         mime_type = SUPPORTED_MIME_TYPES.get(ext)

#     #         if mime_type:
#     #             # Salva o arquivo com o nome original
#     #             save_path = os.path.join("temp_dir", filename)
#     #             file.save(save_path)

#     #             # Faz o upload com o nome original
#     #             with open(save_path, "rb") as f:
#     #                 uploaded = client.files.create(
#     #                     file=f,
#     #                     purpose="assistants"
#     #                 )

#     #             uploaded_file_ids.append({
#     #                 "file_id": uploaded.id,
#     #                 "tools": [{"type": "file_search"}]
#     #             })
#     #             file_descriptions.append(f"✅ Arquivo `{filename}` enviado como `{uploaded.id}`.")
#     #         else:
#     #             logger.info(f"⚠️ Arquivo {filename} ignorado. Tipo MIME '{file.mimetype}' não suportado.")
                
#     # # Recupera o histórico atual da conversa (sem injetar nova mensagem ainda)

#     async def generate_response():
#         print("🧠 Enviando mensagem ao agente de triagem...")
#         # triage_agent = TriageAgent(
#         #     WEBHOOK_URL,
#         #     session_id,
#         #     user_email,
#         # )
        
#         # await process_stream_and_save_history(
           
#         #     triage_agent,
#         #     message,
#         #     WEBHOOK_URL,
#         #     session_id,
#         #     user_email,
#         #     "1",
#         #     appcompany
#         #     )





#     # async def generate_response():
#         # agent = get_agent_for_session(session_id=session_id)
#         # if agent is None:
#         #     agent = Agent(
#         #         name="Chat Agent",
#         #         instructions=instrucoes,
#         #         model="gpt-4o-mini",
#         #         tools=[criar_grafico]
#         #     )
#         #     save_agent_for_session(session_id=session_id, agent=agent)

#         # # 🖼️ Se houver imagens, tratamos com OpenAI vision
#         # if images:
#         #     multimodal_content = [{"type": "text", "text": message}]
#         #     for image_data in image_data_list:
#         #         multimodal_content.append({
#         #             "type": "image_url",
#         #             "image_url": {
#         #                 "url": f"data:{image_data['mime_type']};base64,{image_data['encoded_image']}",
#         #                 "detail": "low"
#         #             }
#         #         })

#         #     # 🔍 Faz a análise da imagem com o modelo vision
#         #     vision_response = client.chat.completions.create(
#         #         model="gpt-4o",
#         #         messages=[
#         #             {"role": "system", "content": "Analise a imagem e descreva os dados importantes."},
#         #             {"role": "user", "content": multimodal_content}
#         #         ],
#         #         store=True
#         #     )

#         #     vision_result = vision_response.choices[0].message.content

#         #     send_to_webhook("Chat Agent", "info", vision_result)

#         #     # Adiciona o resultado da imagem como nova mensagem do usuário
#         #     agent_input.append({
#         #         "role": "system",
#         #         "content": f"Resultado da imagem: {vision_result}",
#         #     })

#         # # 📄 Processamento de arquivos usando Assistants API com file_ids
#         # if files:
#         #     assistant,_,_,_, = create_or_auth_AI(
#         #         key=session_id,
#         #         instructionsassistant=instructions_general_assistant,
#         #         nameassistant="ChatManager",
#         #         model_select="gpt-4o-mini-2024-07-18",
#         #         tools=[{"type": "file_search"}]
#         #     )

#         #     thread = create_or_auth_thread(
#         #         user_id=session_id,
#         #     )

#         #     client.beta.threads.update(
#         #         thread_id=str(thread),
#         #     )
#         #     message_atached = client.beta.threads.messages.create(
#         #                                                         thread_id=thread, 
#         #                                                         role="user", 
#         #                                                         content=message,
#         #                                                         attachments=uploaded_file_ids

#         #                                                         )

              
#         #     run = client.beta.threads.runs.create(
#         #         thread_id=thread,
#         #         assistant_id=assistant,
#         #         tools=[{"type": "file_search"}]
#         #     )
#         #     contador = 0
#         #     logger.info('⏳ Monitoring execution status...')
#         #     i = 0
#         #     for irg in range(900):
#         #         time.sleep(2)
                
#         #         run_status = client.beta.threads.runs.retrieve(
#         #             thread_id=thread,
#         #             run_id=run.id
#         #         )
#         #         if run_status.status == 'completed':
#         #             logger.info('✅ Execution completed successfully.')
#         #             break
#         #         elif run_status.status == 'failed':
#         #             logger.info('❌ Execution failed.')
#         #             break
#         #         elif run_status.status == 'in_progress':
#         #             pontos = '.' * i 
#         #             logger.info(f'💭 Thinking{pontos}')
#         #             i = i + 1 if i < 3 else 1  # Reinicia o contador após 3
#         #         else:
#         #             contador += 1
#         #             if contador == 15:
#         #                 logger.info('⚠️ Tempo limite atingido. Finalizando monitoramento.',
#         #                             '⚠️ Timeout reached. Stopping monitoring.', 'red')
#         #                 break
#         #             logger.info('⏳ Aguardando a execução ser completada...',
#         #                         '⏳ Waiting for execution to complete...', 'cyan')

#         #     logger.info('📨 Retrieving messages from the thread...')

#         #     messages = client.beta.threads.messages.list(thread_id=thread)

#         #     file_id = None
#         #     contador23 = 0

#         #     for message_op in messages:
#         #         for mensagem_contexto in message_op.content:
#         #             logger.info(f'📩 Message received: {mensagem_contexto.text.value}')

#         #             valor_texto = mensagem_contexto.text.value
#         #             logger.info(f"📎 Resultado dos arquivos: {valor_texto}")

#         #             send_to_webhook("Chat Agent", "info", valor_texto)

#         #             agent_input.append({
#         #                 "role": "system",
#         #                 "content": f"Resultado da análise dos arquivos: {valor_texto}"
#         #             })
#         #             price = calculate_dollar_value(run_status.usage.prompt_tokens, run_status.usage.completion_tokens)
#         #             logger.info(f'📜 Tokens consumed : {run_status.usage.total_tokens} 💸${price:.4f}')
#         #             break
#         #         break
                

#     # Evita conflito de loops com interpretador
#     def run_async():
#         try:
#             loop = asyncio.new_event_loop()
#             asyncio.set_event_loop(loop)
#             loop.run_until_complete(generate_response())
#         except Exception as e:
#             logger.info(f"Erro ao rodar stream do agente: {e}")


#     thread = threading.Thread(target=run_async, daemon=True)
#     thread.start()


#     return jsonify({
#         "session_id": session_id,
#     }), 201



@app.route('/api/response-conversation', methods=['POST'])
@limiter.limit(lambda: dynamic_rate_limit(appcompany))
def api_response_conversation():
    message = request.form.get("message")
    session_id = request.form.get("session_id")
    user_email = request.form.get("user_email")

    dir_curent = os.path.join(os.path.dirname(__file__))
    os.chdir(dir_curent)

    api_key = get_api_key()
    usuario, erro = autenticar_usuario(appcompany=appcompany)
    if erro:
        return erro
    
    if not user_email:
        return jsonify({"error": "user_email is required"}), 400
    
    async def generate_response():
        Tools_Name_dict = Egetoolsv2(["make_httprequest", "autoruncodepython"])
        ChatManager_agent = Agent(
            name="ChatManager",
            instructions=f"""
{RECOMMENDED_PROMPT_PREFIX}\n
Meu nome é ChatManager, Sou um pensador que responde mensagens importantes e para isso utilizo cada ferramenta segundo as minhas regras 

Regras:

Regra 1 - Caso seja solicitado algum web site que se enquadre no tipo Saas (software como serviço) realize os passos abaixo

    1 - use a ferramenta autoruncodepython (essa ferramenta retorna quanto o projeto custará aproximadamente )
    2 - use a ferramenta make_httprequest (em name_project crie um nome para o projeto) (depois que usar a ferramenta responda que a equipe do Agent Work flow Saas estará iniciando os trabalhos no projeto e que o usuario pode observar no modal abaixo e o quanto custará aproximadamente a criacao do projeto )  

    autoruncodepython:
        arguments: "nada"
        python_env: python
        script_name: eval_cost_project.py

    make_httprequest:
        method: "POST"
        url: "https://softwareai.rshare.io/api/AgentsWorkFlow/Saas"
        headers: {{
        "X-API-KEY": "{api_key}",
        "X-User-Email": "{user_email}",
        }},
        body: {{
        "session_id": "{session_id}",
        "user_email": "{user_email}",
        "user_message": "{message}",
        "name_project": "Nome_Gerado_Por_Voce",
        }}

Regra 2 - Caso usuario esteja conversando e ou escrevendo apenas converse respondendo nao encaminhe para nenhum agente e nao execute make_httprequest


Regra 3 - Caso usuario diga que concluiu a instalacao da extencao Release Share e retornar uma url do projeto
nao execute make_httprequest e encaminhe para agente 





            """,
            model="o3-mini",
            tools=Tools_Name_dict

        )

        await process_stream_and_save_history(
            "real_stream",
            ChatManager_agent,
            message,
            WEBHOOK_URL,
            session_id,
            user_email,
            "1",
            appcompany
            )

    def run_async():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_response())
        except Exception as e:
            logger.info(f"Erro ao rodar stream do agente: {e}")
    thread = threading.Thread(target=run_async, daemon=True)
    thread.start()


    return jsonify({
        "session_id": session_id,
    }), 201


# @app.route('/api/AgentsWorkFlow/Saas', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))
# def api_AgentsWorkFlow_Saas():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     user_message = data.get("user_message")
#     name_project = data.get("name_project")
#     type_stream = "agentworkflow"

#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro
    
#     if not user_email:
#         return jsonify({"error": "user_email is required"}), 400

#     refuser = db.reference(f'users/{user_email.replace(".", "_")}', app=appcompany)
#     data_user = refuser.get()
#     refsettings = db.reference(f'users/{user_email.replace(".", "_")}/settings', app=appcompany)
#     data_user_settings = refsettings.get()
#     refdashboard = db.reference(f'users/{user_email.replace(".", "_")}/settings/dashboard', app=appcompany)
#     data_user_dashboard = refdashboard.get()
#     refgithub = db.reference(f'users/{user_email.replace(".", "_")}/settings/github', app=appcompany)
#     data_user_github = refgithub.get()
#     github_token = data_user_github.get("github_token")
#     githubCompany = data_user_dashboard.get("githubCompany")
#     STRIPE_SECRET_KEY = data_user_dashboard.get("STRIPE_SECRET_KEY")
#     NEXT_PUBLIC_STRIPE_PUB_KEY = data_user_dashboard.get("NEXT_PUBLIC_STRIPE_PUB_KEY")
#     STRIPE_WEBHOOK_EVENTS = "payout.paid customer.subscription.deleted checkout.session.async_payment_failed checkout.session.async_payment_succeeded checkout.session.expired checkout.session.completed checkout.session.expired invoice.payment_succeeded invoice.paid invoice.finalized invoice.updated payment_intent.created payment_intent.succeeded charge.succeeded"
#     user_credentials_arg = data_user_settings.get("firebase_config")


#     prompt_continuous = "Siga Com os objetivos da instrucao"
#     path_ProjectWeb = f"/app/LocalProject/{name_project}"
#     os.makedirs(path_ProjectWeb, exist_ok=True)
#     os.chdir(path_ProjectWeb)
#     path_html = f"templates"
#     path_js = f"static/js"
#     path_css = f"static/css"
#     doc_md = f"doc_md"
#     Keys_path = f"Keys"
#     os.makedirs(path_html, exist_ok=True)
#     os.makedirs(path_js, exist_ok=True)
#     os.makedirs(path_css, exist_ok=True)
#     os.makedirs(doc_md, exist_ok=True)
#     os.makedirs(Keys_path, exist_ok=True)
    
#     os.chdir(os.path.join(os.path.dirname(__file__)))

#     path_Keys = Keys_path
#     githubtoken = github_token
#     repo_owner = githubCompany
#     user_credentials = user_credentials_arg

#     index_ = '''
# # Rota para a landing page
# @app.route('/')
# def index():
#     return render_template('index.html')
#     '''

#     login = '''
# # Rota para a página de Login
# @app.route('/login')
# def login():
#     return render_template('login.html')
#     '''

#     dashboard = '''
# # Rota para a página de dashboard
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')
#     '''

#     checkout = '''
# # Rota para a página de Checkout de um plano específico
# @app.route('/checkout')
# def checkout():
#     plan_name = request.args.get('plan', 'free')  # Valor padrão 'free'
#     return render_template('checkout.html', plan=plan_name)
#     '''

#     checkout_sucess = '''
# # Rota para exibir uma página de sucesso após o checkout
# @app.route('/checkout/sucess')
# def checkout_sucess():
#     return render_template('success.html')

#     '''

#     basic_endpoints = '''
# import os
# import sys
# import json
# import uuid
# import secrets
# from datetime import timedelta, datetime

# from flask import Flask, render_template, request, redirect, url_for, session, jsonify
# from flask_cors import CORS
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

# import stripe
# import requests
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText

# import logging

# from dotenv import load_dotenv
# from firebase_admin import db
# from Keys.fb import init_firebase


# # Change current working directory to the file's directory
# os.chdir(os.path.join(os.path.dirname(__file__)))

# # Criação da aplicação Flask
# app = Flask(__name__, static_folder='static', template_folder='templates')
# CORS(app, supports_credentials=True, origins="*")

# # Configurações de sessão
# app.secret_key = 'sua_chave_secreta'
# app.permanent_session_lifetime = timedelta(days=7)
# app.config['SESSION_COOKIE_SECURE'] = False
# app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# ###############################################
# # Integração de Código Base para Firebase, dotenv e Stripe
# ###############################################


# app_instance = init_firebase()

# load_dotenv(dotenv_path="Keys/keys.env")

# gmail_usuario = os.getenv("gmail_usuario")
# gmail_senha = os.getenv("gmail_senha")
# stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
# WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
# SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_premium")
# API_BASE_URL = os.getenv("API_BASE_URL")

# ###############################################
# # logging
# ###############################################

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# ###############################################
# # Funções de autenticação e controle de taxa
# ###############################################

# def get_api_key():
#     return request.headers.get('X-API-KEY')


# def key_func():
#     api_key = get_api_key()
#     return api_key if api_key else get_remote_address()


# def generate_api_key(subscription_plan):
#     prefix_map = {{
#         "premium": "apikey-premium",
#     }}
#     prefix = prefix_map.get(subscription_plan.lower(), "apikey-default")
#     unique_part = secrets.token_urlsafe(32)
#     api_key = f"{{prefix}}-{{unique_part}}"
#     return api_key


# # Configuração do Limiter para controle de taxa (bloqueia spam apenas para tentativas inválidas)
# limiter = Limiter(
#     app=app,
#     key_func=key_func,
#     default_limits=["10 per minute"]
# )



# ###############################################
# # Rotas da aplicação
# ###############################################

# # Rota para a landing page
# @app.route('/')
# def index():
#     return render_template('index.html')

# # Rota para a página de Login
# @app.route('/login')
# def login():
#     return render_template('loginAndRegistrer.html')

# # Rota para a página de dashboard
# @app.route('/dashboard')
# def dashboard():
#     return render_template('dashboard.html')

# # Rota para a página de Checkout de um plano específico
# @app.route('/checkout')
# def checkout():
#     plan_name = request.args.get('plan', 'free')  # 'free' como valor padrão
#     return render_template('checkout.html', plan=plan_name)

# # Rota para exibir uma página de sucesso após o checkout
# @app.route('/checkout/sucess')
# def checkout_sucess():
#     return render_template('success.html')


#     '''

#     api_create_checkout = '''
    
# ###############################################
# # Endpoint de criação de Checkout (/api/create-checkout)
# ###############################################

# @app.route('/api/create-checkout', methods=['POST'])
# @limiter.limit("10 per minute")
# def create_checkout():
#     data = request.get_json()
#     try:
#         # Calcula a data de expiração: data atual + 31 dias
#         expiration_time = datetime.now() + timedelta(days=31)

#         checkout_session = stripe.checkout.Session.create(
#             line_items=[{
#                 "price": SUBSCRIPTION_PRICE_ID,  # Usando o ID do preço definido no .env
#                 "quantity": 1
#             }],
#             mode="subscription",  # Modo de assinatura
#             payment_method_types=["card"],
#             success_url=f"{API_BASE_URL}/checkout/sucess",  
#             cancel_url=f"{API_BASE_URL}/checkout/cancel",  
#             metadata={
#                 "email": data.get("email"),
#                 "password": data.get("password"),
#                 "SUBSCRIPTION_PLAN": "premium",
#                 "TIMESTAMP": expiration_time.isoformat()
#             },
#         )
#         logger.info("Sessão criada: %s", checkout_session.id)
#         return jsonify({"sessionId": checkout_session.id})
#     except Exception as e:
#         logger.info("Erro ao criar a sessão de checkout: %s", str(e))
#         return jsonify({"error": str(e)}), 500

#     '''

#     api_register = '''

# ###############################################
# # Endpoint de Registro de Usuário (/api/register)
# ###############################################

# @app.route('/api/register', methods=['POST'])
# @limiter.limit("10 per minute")
# def register():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")
#     SUBSCRIPTION_PLAN = data.get("SUBSCRIPTION_PLAN")
#     expiration = data.get("expiration")
#     WEBHOOK_SECRET_flag = data.get("WEBHOOK_SECRET_flag")

#     if not email or not password:
#         return jsonify({"error": "Email e senha são obrigatórios"}), 400

#     if not SUBSCRIPTION_PLAN:
#         SUBSCRIPTION_PLAN = "free"
#     if not expiration:
#         expiration = "None"

#     if SUBSCRIPTION_PLAN == "free":
#         limit = "2 per day"
#     elif SUBSCRIPTION_PLAN == "premium":
#         limit = "50 per day"

#     email_safe = email.replace('.', '_')
#     ref = db.reference(f'users/{email_safe}', app=app_instance)

#     if ref.get():
#         if not WEBHOOK_SECRET_flag:
#             return jsonify({"error": "Voce ja tem uma conta"}), 400

#         if WEBHOOK_SECRET_flag == WEBHOOK_SECRET:
#             api_key = generate_api_key(SUBSCRIPTION_PLAN)
#             ref.update({
#                 "api_key": api_key,
#                 "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
#                 "limit": limit,
#                 "expiration": expiration
#             })
#             return jsonify({
#                 "message": "Upgrade realizado",
#                 "email": email,
#                 "password": password,
#                 "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
#                 "limit": limit,
#                 "expiration": expiration,
#                 "api_key": api_key
#             }), 409

#     api_key = generate_api_key(SUBSCRIPTION_PLAN)
#     ref.set({
#         "email": email,
#         "password": password,
#         "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
#         "limit": limit,
#         "expiration": expiration,
#         "api_key": api_key,
#         "created_at": datetime.now().isoformat()
#     })
#     return jsonify({
#         "message": "Usuário registrado com sucesso",
#         "email": email,
#         "password": password,
#         "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
#         "limit": limit,
#         "expiration": expiration,
#         "api_key": api_key,
#         "created_at": datetime.now().isoformat()
#     }), 200

#     '''

#     api_login = '''

# ###############################################
# # Endpoint de Login (/api/login)
# ###############################################

# @app.route('/api/login', methods=['POST'])
# def apilogin():
#     data = request.get_json()
#     email = data.get("email")
#     password = data.get("password")

#     if not email or not password:
#         return jsonify({"error": "Email e senha são obrigatórios"}), 400

#     email_safe = email.replace('.', '_')
#     user = db.reference(f'users/{email_safe}', app=app_instance).get()

#     if not user:
#         return jsonify({"error": "Usuário não encontrado"}), 404

#     if user.get("password") != password:
#         return jsonify({"error": "Senha incorreta"}), 401

#     session['user'] = email
#     session.permanent = True  # <- IMPORTANTE

#     return jsonify({"message": "Login realizado com sucesso"}), 200

#     '''

#     webhook = '''

# ###############################################
# # Endpoint do Webhook (/webhook)
# ###############################################

# @app.route("/webhook", methods=["POST"])
# @limiter.limit("10 per minute")
# def stripe_webhook():
#     """
#     Endpoint para tratar os webhooks enviados pela Stripe.
#     """
#     payload = request.data
#     sig_header = request.headers.get("Stripe-Signature")
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(payload, sig_header, WEBHOOK_SECRET)
#     except ValueError as e:
#         logger.info("Payload inválido")
#         return jsonify({"message": "Invalid payload"}), 400
#     except stripe.error.SignatureVerificationError as e:
#         logger.info("Assinatura inválida")
#         return jsonify({"message": "Invalid signature"}), 400

#     # Processa o evento conforme o seu tipo 
#     if event["type"] == "checkout.session.completed":
#         session_data = event["data"]["object"]
#         if session_data.get("payment_status") == "paid":
#             email = session_data["metadata"].get("email")
#             password = session_data["metadata"].get("password")
#             SUBSCRIPTION_PLAN = session_data["metadata"].get("SUBSCRIPTION_PLAN")
#             TIMESTAMP = session_data["metadata"].get("TIMESTAMP")
#             logger.info("Pagamento por cartão com sucesso: %s, %s", email, SUBSCRIPTION_PLAN)

#             data = {
#                 "email": email,
#                 "password": password,
#                 "WEBHOOK_SECRET_flag": WEBHOOK_SECRET,
#                 "SUBSCRIPTION_PLAN": SUBSCRIPTION_PLAN,
#                 "expiration": TIMESTAMP,
#             }
#             headers = {
#                 "Content-Type": "application/json",
#                 "X-API-KEY": os.getenv("ADMIN_API_KEY", "default_api_key")
#             }
#             API_BASE_URL = os.getenv("API_BASE_URL")
#             response = requests.post(f"{API_BASE_URL}/api/register", json=data, headers=headers)

#             if response.status_code == 200:
#                 response_data = response.json()
#                 message = response_data.get("message")
#                 login_val = response_data.get("email")
#                 password_val = response_data.get("password")
#                 expiration = response_data.get("expiration")
#                 subscription_plan = response_data.get("SUBSCRIPTION_PLAN")
#                 api_key = response_data.get("api_key")

#                 logger.info(f"Mensagem: {message}")
#                 logger.info(f"Login: {login_val}")
#                 logger.info(f"Senha: {password_val}")
#                 logger.info(f"Expiração: {expiration}")
#                 logger.info(f"Plano de assinatura: {subscription_plan}")

#                 # Cria e envia o e-mail
#                 from email.mime.multipart import MIMEMultipart
#                 from email.mime.text import MIMEText
#                 import smtplib

#                 msg = MIMEMultipart()
#                 msg["From"] = gmail_usuario
#                 msg["To"] = email
#                 msg["Subject"] = "SoftwareAI"

#                 corpo = f"""
# 😀 Hello Here is your login, Thank you for choosing SoftwareAI

# 📱 Support Groups:
# ✨Discord:
# ✨Telegram:

# 💼 Chat Panel:
# 📌Login: {login_val}
# 📌Password: {password_val}

# 💼 Info Account:
# 📌api key: {api_key}
# 📌Expiration: {expiration}
# 📌Subscription plan: {subscription_plan}
#                 """
#                 msg.attach(MIMEText(corpo, "plain"))

#                 try:
#                     servidor = smtplib.SMTP("smtp.gmail.com", 587)
#                     servidor.starttls()
#                     servidor.login(gmail_usuario, gmail_senha)
#                     servidor.sendmail(gmail_usuario, email, msg.as_string())
#                     servidor.quit()
#                     logger.info("E-mail enviado com sucesso!")
#                 except Exception as e:
#                     logger.info(f"Erro ao enviar e-mail: {e}")

#             elif response.status_code == 409:
#                 logger.info("Parece que o usuario ja tem uma conta e possivelmente esta tentando atualizar para o premium")
#                 response_data = response.json()

#                 message = response_data.get("message")
#                 login_val = response_data.get("email")
#                 password_val = response_data.get("password")
#                 expiration = response_data.get("expiration")
#                 subscription_plan = response_data.get("SUBSCRIPTION_PLAN")
#                 api_key = response_data.get("api_key")

#                 logger.info(f"Mensagem: {message}")
#                 logger.info(f"Login: {login_val}")
#                 logger.info(f"Senha: {password_val}")
#                 logger.info(f"Expiração: {expiration}")
#                 logger.info(f"Plano de assinatura: {subscription_plan}")

#                 # Cria e envia o e-mail de upgrade
#                 from email.mime.multipart import MIMEMultipart
#                 from email.mime.text import MIMEText
#                 import smtplib

#                 msg = MIMEMultipart()
#                 msg["From"] = gmail_usuario
#                 msg["To"] = email
#                 msg["Subject"] = "SoftwareAI"

#                 corpo = f"""
# 😀 Hi, Your account has been upgraded. Thank you for choosing and trusting SoftwareAI

# 📱 Support Groups:
# ✨Discord:
# ✨Telegram:

# 💼 Chat Panel:
# 📌Login: {login_val}
# 📌Password: {password_val}

# 💼 Account Information:
# 📌API Key: {api_key}
# 📌Expiration: {expiration}
# 📌Subscription Plan: {subscription_plan}
#                 """
#                 msg.attach(MIMEText(corpo, "plain"))

#                 try:
#                     servidor = smtplib.SMTP("smtp.gmail.com", 587)
#                     servidor.starttls()
#                     servidor.login(gmail_usuario, gmail_senha)
#                     servidor.sendmail(gmail_usuario, email, msg.as_string())
#                     servidor.quit()
#                     logger.info("E-mail enviado com sucesso!")
#                 except Exception as e:
#                     logger.info(f"Erro ao enviar e-mail: {e}")

#         elif session_data.get("payment_status") == "unpaid" and session_data.get("payment_intent"):
#             payment_intent = stripe.PaymentIntent.retrieve(session_data["payment_intent"])
#             hosted_voucher_url = (payment_intent.next_action and payment_intent.next_action.get("boleto_display_details", {}).get("hosted_voucher_url"))
#             if hosted_voucher_url:
#                 user_email = session_data.get("customer_details", {}).get("email")
#                 logger.info("Gerou o boleto e o link é %s", hosted_voucher_url)

#     elif event["type"] == "checkout.session.expired":
#         session_data = event["data"]["object"]
#         if session_data.get("payment_status") == "unpaid":
#             teste_id = session_data["metadata"].get("testeId")
#             logger.info("Checkout expirado %s", teste_id)

#     elif event["type"] == "checkout.session.async_payment_succeeded":
#         session_data = event["data"]["object"]
#         if session_data.get("payment_status") == "paid":
#             teste_id = session_data["metadata"].get("testeId")
#             logger.info("Pagamento boleto confirmado %s", teste_id)

#     elif event["type"] == "checkout.session.async_payment_failed":
#         session_data = event["data"]["object"]
#         if session_data.get("payment_status") == "unpaid":
#             teste_id = session_data["metadata"].get("testeId")
#             logger.info("Pagamento boleto falhou %s", teste_id)

#     elif event["type"] == "customer.subscription.deleted":
#         logger.info("Cliente cancelou o plano")

#     return jsonify({"result": event, "ok": True})

#     '''




#     checkout_payment_button = f"""

# document.addEventListener("DOMContentLoaded", function() {{
# const urlParams = new URLSearchParams(window.location.search);
# const planParam = urlParams.get("plan");

# let plano;

# if (planParam === "free") {{
#     window.location.href = `/login`;
# }} else {{
#     plano = planParam;
# }}

# const payNowButton = document.querySelector('.block-pay-now .btn-primary');
# const loadingSpinner = document.querySelector('.loading-spinner');

# if (payNowButton) {{
#     payNowButton.addEventListener("click", function() {{
#     // Exibe o spinner de carregamento
#     loadingSpinner.style.display = 'block';

#     const selectedOption = document.querySelector('.option.selected');
    
#     if (selectedOption) {{
#         const paymentMethod = selectedOption.getAttribute("data-method");
#         const email = document.querySelector('.email-input').value;
#         const password = document.querySelector('.password-input').value;

#         if (!email) {{
#         alert("Por favor, insira seu email.");
#         loadingSpinner.style.display = 'none';
#         return; 
#         }}

#         fetch("/api/create-checkout", {{
#         method: "POST",
#         headers: {{
#             "Content-Type": "application/json"
#         }},
#         body: JSON.stringify({{
#             email: email,
#             password: password,
#             plano: plano          
#         }}),
#         }})
#         .then(response => {{
#         console.log("Resposta do servidor:", response);
        
#         if (!response.ok) {{
#             throw new Error("Erro na requisição. Status: " + response.status);
#         }}
#         return response.json()
#             .catch(error => {{
#             console.error("Erro ao converter a resposta para JSON:", error);
#             throw new Error("Erro ao converter a resposta para JSON");
#             }});
#         }})
#         .then(data => {{
#         console.log("Dados recebidos:", data);
#         loadingSpinner.style.display = 'none';
        
#         if (data.sessionId) {{
#             const stripe = Stripe("{NEXT_PUBLIC_STRIPE_PUB_KEY}");
#             stripe.redirectToCheckout({{ sessionId: data.sessionId }})
#             .then(() => {{
#             window.location.href = "/checkout/sucess";
#             }});
#         }} else {{
#             alert("Erro ao criar a sessão de pagamento.");
#         }}
#         }})
#         .catch(error => {{
#         console.error("Erro ao enviar a requisição:", error);
#         alert("Erro ao processar o pagamento.");
#         loadingSpinner.style.display = 'none';
#         }});
#     }} else {{
#         alert("Por favor, selecione um método de pagamento.");
#         loadingSpinner.style.display = 'none';
#     }}
#     }});
# }}
# }});


#     """

#     checkout_payment_selected = """
# document.addEventListener("DOMContentLoaded", function() {
# const paymentOptions = document.querySelectorAll('.option');

# paymentOptions.forEach(function(option) {
#     option.addEventListener("click", function() {
#     // Remove a classe 'selected' de todas as opções
#     paymentOptions.forEach(function(opt) {
#         opt.classList.remove("selected");
#     });
    
#     // Adiciona a classe 'selected' na opção clicada
#     option.classList.add("selected");
    
#     // Loga o método de pagamento selecionado
#     const selectedMethod = option.getAttribute("data-method");
#     console.log("Método selecionado:", selectedMethod);
#     });
# });
# });

#     """
    
#     loginAndRegistrer = """
# document.addEventListener("DOMContentLoaded", () => {
# const msg = document.getElementById('msg');
# const loginEmail = document.getElementById('login-email');
# const loginPassword = document.getElementById('login-password');

# const registerName = document.getElementById('register-name');
# const registerEmail = document.getElementById('register-email');
# const registerPassword = document.getElementById('register-password');

# function showMessage(text, color = "red") {
#     msg.textContent = text;
#     msg.style.color = color;
# }

# window.toggleForms = function() {
#     const loginForm = document.getElementById('login-form');
#     const registerForm = document.getElementById('register-form');
#     if (loginForm.style.display === 'none') {
#     loginForm.style.display = 'block';
#     registerForm.style.display = 'none';
#     } else {
#     loginForm.style.display = 'none';
#     registerForm.style.display = 'block';
#     }
#     showMessage("");
# };

# window.togglePassword = function(inputId, toggleIcon) {
#     const input = document.getElementById(inputId);
#     if (input.type === 'password') {
#     input.type = 'text';
#     toggleIcon.textContent = '🙈';
#     } else {
#     input.type = 'password';
#     toggleIcon.textContent = '👁️';
#     }
# };

# document.getElementById('login-btn').addEventListener('click', () => {
#     const email = loginEmail.value.trim();
#     const password = loginPassword.value;

#     if (!email || !password) {
#     return showMessage('Preencha todos os campos de login!');
#     }

#     showMessage('Carregando...', 'blue');
#     fetch('/api/login', {
#     method: 'POST',
#     headers: { 'Content-Type': 'application/json' },
#     credentials: 'include',
#     body: JSON.stringify({ email, password })
#     })
#     .then(res => res.json())
#     .then(data => {
#     if (data.error) return showMessage(data.error);
#     showMessage('Login realizado com sucesso!', 'green');
#     localStorage.setItem('userEmail', email);
#     localStorage.setItem('user_email', email);
#     setTimeout(() => {
#         window.location.href = '/dashboard';
#     }, 1000);
#     })
#     .catch(err => showMessage('Erro de rede'));
# });

# document.getElementById('register-btn').addEventListener('click', () => {
#     const name = registerName.value.trim();
#     const email = registerEmail.value.trim();
#     const password = registerPassword.value;

#     if (!name || !email || !password) {
#     return showMessage('Preencha todos os campos de cadastro!');
#     }

#     showMessage('Carregando...', 'blue');
#     fetch('/api/register', {
#     method: 'POST',
#     headers: { 'Content-Type': 'application/json' },
#     body: JSON.stringify({ name, email, password })
#     })
#     .then(res => res.json())
#     .then(data => {
#     if (data.error) return showMessage(data.error);
#     showMessage('Registro realizado com sucesso!', 'green');
#     localStorage.setItem('userEmail', email);
#     setTimeout(() => {
#         window.location.href = '/dashboard';
#     }, 1000);
#     })
#     .catch(err => showMessage('Erro de rede'));
# });
# });

#     """
    
#     navigation_js = """

#     """
    
#     landing = """
# /* landing.js - Refatoração do código inline presente no index.html para melhorar a modularidade e a organização do JavaScript da landing page. */

# document.addEventListener('DOMContentLoaded', () => {
# // Função para manipulação do menu mobile
# function initMobileMenu() {
#     const menuToggle = document.getElementById('mobile-menu');
#     const navLinks = document.getElementById('nav-links');
#     if (!menuToggle || !navLinks) {
#     console.error('Elementos do menu mobile não encontrados.');
#     return;
#     }
#     menuToggle.addEventListener('click', () => {
#     navLinks.classList.toggle('active');
#     });
# }

# // Função para scroll suave ao clicar nos links do menu
# function initSmoothScrolling() {
#     const navAnchors = document.querySelectorAll('.nav-links a');
#     const navLinks = document.getElementById('nav-links');

#     navAnchors.forEach(anchor => {
#     anchor.addEventListener('click', function(e) {
#         e.preventDefault();
#         const targetSelector = this.getAttribute('href');
#         const targetElement = document.querySelector(targetSelector);
#         if (targetElement) {
#         targetElement.scrollIntoView({ behavior: 'smooth' });
#         } else {
#         console.error(`Elemento destino '${targetSelector}' não encontrado.`);
#         }
#         if (navLinks && navLinks.classList.contains('active')) {
#         navLinks.classList.remove('active');
#         }
#     });
#     });
# }

# // Função para o comportamento de acordeão na seção FAQ
# function initFAQAccordion() {
#     const faqItems = document.querySelectorAll('.faq-item');
#     if (!faqItems.length) {
#     console.error('Nenhum item de FAQ encontrado.');
#     return;
#     }
#     faqItems.forEach(item => {
#     item.addEventListener('click', () => {
#         item.classList.toggle('active');
#     });
#     });
# }

# // Função para o slider de depoimentos
# function initTestimonialSlider() {
#     const testimonials = document.querySelectorAll('.testimonial');
#     const controlsContainer = document.getElementById('slider-controls');
#     if (!testimonials.length || !controlsContainer) {
#     console.error('Depoimentos ou controles do slider não encontrados.');
#     return;
#     }
#     const controls = controlsContainer.children;
#     let currentTestimonial = 0;

#     function showTestimonial(index) {
#     testimonials.forEach((testimonial, i) => {
#         testimonial.style.display = (i === index) ? 'block' : 'none';
#     });
#     Array.from(controls).forEach(control => control.classList.remove('active'));
#     if (controls[index]) controls[index].classList.add('active');
#     }

#     showTestimonial(currentTestimonial);

#     Array.from(controls).forEach(control => {
#     control.addEventListener('click', (e) => {
#         const index = parseInt(e.target.getAttribute('data-index'));
#         if (!isNaN(index)) {
#         currentTestimonial = index;
#         showTestimonial(currentTestimonial);
#         } else {
#         console.error('Índice inválido para o slider de depoimentos.');
#         }
#     });
#     });

#     // Auto slide a cada 5 segundos
#     setInterval(() => {
#     currentTestimonial = (currentTestimonial + 1) % testimonials.length;
#     showTestimonial(currentTestimonial);
#     }, 5000);
# }

# // Inicializa todas as funções
# initMobileMenu();
# initSmoothScrolling();
# initFAQAccordion();
# initTestimonialSlider();
# });


#     """
    
#     script_base_login_js = '''
# const emailInput = document.getElementById('email');
# const passwordInput = document.getElementById('password');
# const msg = document.getElementById('msg');

# function showMessage(text, color = "red") {
# msg.textContent = text;
# msg.className = `text-sm text-center text-${{color}}-400`;
# }
# document.addEventListener("DOMContentLoaded", () => {
# document.getElementById('login-btn').addEventListener('click', () => {
#     const email = emailInput.value.trim();
#     const password = passwordInput.value;
#     const api_url_login = "/api/login";
#     fetch(api_url_login, {
#     method: 'POST',
#     headers: { 'Content-Type': 'application/json' },
#     credentials: 'include',  // 👈 necessário para manter a sessã
#     body: JSON.stringify({ email, password })
#     })
#     .then(res => res.json())
#     .then(data => {
#     if (data.error) return showMessage(data.error);
    
#     showMessage("Login realizado com sucesso!", "green");

#     // ✅ Armazena email para uso futuro se quiser
#     localStorage.setItem("userEmail", email);
#     localStorage.setItem("user_email", email);
    
#     // ✅ Redireciona após login, se necessário
#     setTimeout(() => {
#         window.location.href = "/dashboard";
#     }, 1000);
#     })
#     .catch(err => showMessage("Erro de rede"));
# });

# document.getElementById('register-btn').addEventListener('click', () => {
#     const email = emailInput.value.trim();
#     const password = passwordInput.value;
#     const api_url_register = "/api/register";
#     fetch(api_url_register, {
#         method: 'POST',
#         headers: { 'Content-Type': 'application/json' },
#         body: JSON.stringify({ email, password })
#     })
#     .then(res => res.json())
#     .then(data => {
#         if (data.error) return showMessage(data.error);
        
#         showMessage("Registro realizado com sucesso!", "green");
    
#         // ✅ Armazena email para uso futuro se quiser
#         localStorage.setItem("userEmail", email);
    
#         // ✅ Redireciona após login, se necessário
#         setTimeout(() => {
#         window.location.href = "/dashboard";
#         }, 1000);
#     })
#     .catch(err => showMessage("Erro de rede"));
# });
# });

# '''

#     user_code_init_env = f'''
# STRIPE_WEBHOOK_SECRET=
# STRIPE_SECRET_KEY={STRIPE_SECRET_KEY}
# STRIPE_SUBSCRIPTION_PRICE_ID_Premium=
# NEXT_PUBLIC_STRIPE_PUB_KEY={NEXT_PUBLIC_STRIPE_PUB_KEY}
# gmail_usuario=
# gmail_senha=
# API_BASE_URL="http://127.0.0.1:5000"

#     '''

#     docker_file = f"""
# FROM python:3.12-slim
# RUN apt-get update && \
#     apt-get install -y \
#     git

# # Install Node.js 22.x (needed for codex CLI)
# RUN apt-get update && \
#     apt-get install -y curl gnupg ca-certificates && \
#     curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
#     apt-get install -y nodejs && \
#     rm -rf /var/lib/apt/lists/*

# # Install codex CLI globally
# RUN npm install -g @openai/codex

# WORKDIR /app

# COPY requirements.txt requirements.txt
# RUN pip install --no-cache-dir -r requirements.txt

# RUN git init /app

# # Copiar todos os arquivos do projeto
# COPY . /app



#     """
   

#     docker_compose_file = f"""
# version: '3.8'

# services:
#   landingpage:
#     build: .
#     container_name: landingpageapp
#     restart: always
#     ports:
#       - "5000:5000"
#     volumes:
#       - .:/app
#       - /var/run/docker.sock:/var/run/docker.sock
#     command: >
#       sh -c "python app.py"
#     mem_limit: 500MB
#     cpus: "1.5"


#     """
   
   
   
#     async def generate_response():
#         print("🧠 Enviando mensagem ao agente de triagem...")

#         # /api/AgentsWorkFlow/Saas/teams/ProjectManager V

#         # /api/AgentsWorkFlow/Saas/teams/FrontEnd V

#         # /api/AgentsWorkFlow/Saas/teams/BackEnd V

#         # /api/AgentsWorkFlow/Saas/teams/DevOps/Docker V

#         # /api/AgentsWorkFlow/Saas/teams/Documentation V

#         # /api/AgentsWorkFlow/Saas/teams/DevOps/RunBuild V

#         # /api/AgentsWorkFlow/Saas/teams/DevOps/EasyDeploy V

#         # /api/AgentsWorkFlow/Saas/teams/DevOps/UploadGit V

#         # /api/AgentsWorkFlow/Saas/teams/QA 

#         # /api/AgentsWorkFlow/Saas/teams/ProductManager



        


#     # # Evita conflito de loops com interpretador
#     # def run_async():
#     #     try:
#     #         loop = asyncio.new_event_loop()
#     #         asyncio.set_event_loop(loop)
#     #         loop.run_until_complete(generate_response())
#     #     except Exception as e:
#     #         print(f"Erro ao rodar stream do agente: {e}")


#     # thread = threading.Thread(target=run_async, daemon=True)
#     # thread.start()

#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201


# @app.route('/api/AgentsWorkFlow/Saas/teams/ProjectManager', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))
# def api_AgentsWorkFlow_Saas_teams_ProjectManager(): 
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     user_message = data.get("user_message")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")

#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():


#         async def _project_manager_logic(data, appcompany):
#             session_id = data["session_id"]
#             # return {"step": "ProjectManager", "session_id": session_id}
#             user_email = data["user_email"]
#             agent = TriageAgent(
#                 session_id, user_email,
#                 path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys
#             )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["user_message"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "ProjectManager", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "ProjectManager",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _code_review_preproject_logic(data, appcompany):
#             session_id = data["session_id"]
#             # return {"step": "ProjectManager", "session_id": session_id}
#             session_id         = data["session_id"]
#             user_email         = data["user_email"]
#             prompt_continuous  = data.get("prompt_continuous", "")
#             agent, _ = CodeReview_Preproject(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 path_Keys,
#                                 data["user_message"]
#                                 )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_CodeReview_Preproject", appcompany
#                     )
#                     return {"step": "CodeReview_Preproject", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeReview_Preproject",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _code_requirements_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeRequirementsAndTimeline(
#                 session_id, user_email,
#                 path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys
#             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_CodeRequirementsAndTimeline", appcompany
#                     )
#                     return {"step": "CodeRequirementsAndTimeline", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeRequirementsAndTimeline",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _code_review_timeline_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeReview_Timeline(
#                 session_id, user_email,
#                 path_ProjectWeb, path_html, path_js, path_css, doc_md, path_Keys
#             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_CodeReview_Timeline", appcompany
#                     )
#                     return {"step": "CodeReview_Timeline", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeReview_Timeline",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         def run_project_manager(data, appcompany):
#             return asyncio.run(_project_manager_logic(data, appcompany))

#         def run_code_review_preproject(data, appcompany):
#             return asyncio.run(_code_review_preproject_logic(data, appcompany))

#         def run_code_requirements(data, appcompany):
#             return asyncio.run(_code_requirements_logic(data, appcompany))

#         def run_code_review_timeline(data, appcompany):
#             return asyncio.run(_code_review_timeline_logic(data, appcompany))


#         data = {
#             "session_id": session_id,
#             "user_email": user_email,
#             "user_message": user_message,
#             "prompt_continuous": prompt_continuous,
#         }

#         results = []
#         try:
#             results.append(run_project_manager(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_code_review_preproject(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_code_requirements(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()
#         try:
#             results.append(run_code_review_timeline(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201


# @app.route('/api/AgentsWorkFlow/Saas/teams/FrontEnd', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany)) 
# def api_AgentsWorkFlow_Saas_teams_FrontEnd():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     script_base_login_js = data.get("script_base_login_js")
#     checkout_payment_button = data.get("checkout_payment_button")
#     checkout_payment_selected = data.get("checkout_payment_selected")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     user_code_init_env = data.get("user_code_init_env")
#     firebase_db_url = data.get("firebase_db_url")
#     user_credentials = data.get("user_credentials")
#     prompt_continuous = data.get("prompt_continuous")

#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():


#         async def _CodeIndexFrontEnd_logic(data, appcompany):
#             session_id = data["session_id"]
#             user_email = data["user_email"]
#             agent, _ = CodeIndexFrontEnd(
#                     session_id,
#                     user_email,
#                     path_ProjectWeb,
#                     path_html,
#                     path_js,
#                     path_css,
#                     doc_md,
#                     Keys_path,
#             )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["prompt_continuous"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "CodeIndexFrontEnd", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "CodeIndexFrontEnd",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeLoginFrontEnd_logic(data, appcompany):
#             session_id         = data["session_id"]
#             user_email         = data["user_email"]
#             prompt_continuous  = data.get("prompt_continuous", "")
#             agent, _ = CodeLoginFrontEnd(
#                                     "", 
#                                     "",
#                                     path_ProjectWeb,
#                                     path_html,
#                                     path_js,
#                                     path_css,
#                                     doc_md,
#                                     Keys_path,
#                                     script_base_login_js,
        

#                                 )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeLoginFrontEnd", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeLoginFrontEnd",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeCheckoutFrontEnd_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeCheckoutFrontEnd(
#                         session_id, 
#                         appcompany,
#                         path_ProjectWeb,
#                         path_html,
#                         path_js,
#                         path_css,
#                         doc_md,
#                         Keys_path,
#                         checkout_payment_button,
#                         checkout_payment_selected,
#                     )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeCheckoutFrontEnd", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeCheckoutFrontEnd",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeNavigationJSFrontEnd_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeNavigationJSFrontEnd(
#                                 session_id, 
#                                 appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                                 checkout_payment_button,
#                                 checkout_payment_selected,
#                             )


#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeNavigationJSFrontEnd", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeNavigationJSFrontEnd",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeFrontEndDecisionDashboard_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeFrontEndDecisionDashboard(
#                                     "", 
#                                     "",
#                                     path_ProjectWeb,
#                                     path_html,
#                                     path_js,
#                                     path_css,
#                                     doc_md,
#                                     Keys_path,
#                         )


#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeFrontEndDecisionDashboard", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeFrontEndDecisionDashboard",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeReviewFrontEndHtmlAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeReviewFrontEndHtmlAgent(                                
#                                         session_id, 
#                                         appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         script_base_login_js,
#                                         checkout_payment_button,
#                                         checkout_payment_selected,
#                             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeReviewFrontEndHtmlAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeReviewFrontEndHtmlAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeKeysenvAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeFlaskBackEndKeysenvAgent(                                
#                                         session_id, 
#                                         appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         user_code_init_env
#                             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeFlaskBackEndKeysenvAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeFlaskBackEndKeysenvAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeReviewKeysAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeReviewKeysAgent(session_id, appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         user_code_init_env,
#                                     )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeReviewKeysAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeReviewKeysAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         def run_CodeIndexFrontEnd(data, appcompany):
#             return asyncio.run(_CodeIndexFrontEnd_logic(data, appcompany))

#         def run_CodeLoginFrontEnd(data, appcompany):
#             return asyncio.run(_CodeLoginFrontEnd_logic(data, appcompany))

#         def run_CodeCheckoutFrontEnd(data, appcompany):
#             return asyncio.run(_CodeCheckoutFrontEnd_logic(data, appcompany))

#         def run_CodeNavigationJSFrontEnd(data, appcompany):
#             return asyncio.run(_CodeNavigationJSFrontEnd_logic(data, appcompany))

#         def run_CodeFrontEndDecisionDashboard(data, appcompany):
#             return asyncio.run(_CodeFrontEndDecisionDashboard_logic(data, appcompany))

#         def run_CodeReviewFrontEndHtmlAgent(data, appcompany):
#             return asyncio.run(_CodeReviewFrontEndHtmlAgent_logic(data, appcompany))

#         def run_CodeKeysenvAgent(data, appcompany):
#             return asyncio.run(_CodeKeysenvAgent_logic(data, appcompany))

#         def run_CodeReview_Keys(data, appcompany):
#             return asyncio.run(_CodeReviewKeysAgent_logic(data, appcompany))



#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }

#         appcmp     = appcompany
#         session_id = data.get("session_id", "")

#         results = []


#         try:
#             results.append(run_CodeIndexFrontEnd(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeLoginFrontEnd(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeKeysenvAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()
                
#         CodeFlaskBackEnd_Keys_fb_STATIC(
#                                     user_credentials,
#                                     firebase_db_url,
#                                     session_id, appcompany,
#                                     path_ProjectWeb,
#                                     path_html,
#                                     path_js,
#                                     path_css,
#                                     doc_md,
#                                     Keys_path,
#                                     user_code_init_env,
#                                 )
#         print(f"🤖 Sistema de credenciais firebase executado")

#         try:
#             results.append(run_CodeReview_Keys(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeCheckoutFrontEnd(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeNavigationJSFrontEnd(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeFrontEndDecisionDashboard(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#         try:
#             results.append(run_CodeReviewFrontEndHtmlAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201

# @app.route('/api/AgentsWorkFlow/Saas/teams/BackEnd', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))  
# def api_AgentsWorkFlow_Saas_teams_BackEnd():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     basic_endpoints = data.get("basic_endpoints")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     createcheckout = data.get("createcheckout")
#     api_register = data.get("api_register")
#     api_login = data.get("api_login")
#     code_webhook = data.get("code_webhook")
#     index_ = data.get("index_")
#     checkout = data.get("checkout")
#     checkout_sucess = data.get("checkout_sucess")
#     api_create_checkout = data.get("api_create_checkout")
#     webhook = data.get("webhook")

#     prompt_continuous = data.get("prompt_continuous")


#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }


#         async def _CodeFlaskBackEnd_basic_endpointsAgent_logic(data, appcompany):
#             session_id = data["session_id"]
#             user_email = data["user_email"]
#             agent, _ = CodeFlaskBackEnd_basic_endpointsAgent(                                
#                                             "session_id", 
#                                             "appcompany",
#                                             path_ProjectWeb,
#                                             path_html,
#                                             path_js,
#                                             path_css,
#                                             doc_md,
#                                             Keys_path,
#                                             basic_endpoints
#                                 )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["prompt_continuous"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "CodeFlaskBackEnd_basic_endpointsAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "CodeFlaskBackEnd_basic_endpointsAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeFlaskBackEndapi_create_checkoutAgent_logic(data, appcompany):
#             session_id         = data["session_id"]
#             user_email         = data["user_email"]
#             prompt_continuous  = data.get("prompt_continuous", "")
#             agent, _ = CodeFlaskBackEndapi_create_checkoutAgent(                                
#                                         session_id, 
#                                         appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         createcheckout

#                             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeFlaskBackEndapi_create_checkoutAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeFlaskBackEndapi_create_checkoutAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeFlaskBackEndapi_registerAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeFlaskBackEndapi_registerAgent(                                
#                                         session_id, 
#                                         appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         api_register,

#                             )
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeFlaskBackEndapi_registerAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeFlaskBackEndapi_registerAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeFlaskBackEndapi_loginAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeFlaskBackEndapi_loginAgent(                                
#                                         session_id, 
#                                         appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         api_login

#                             )
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeFlaskBackEndapi_loginAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeFlaskBackEndapi_loginAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeFlaskBackEndwebhookAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeFlaskBackEndwebhookAgent(                                
#                                         session_id, 
#                                         appcompany,
#                                         path_ProjectWeb,
#                                         path_html,
#                                         path_js,
#                                         path_css,
#                                         doc_md,
#                                         Keys_path,
#                                         code_webhook

#                             )


#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeFlaskBackEndwebhookAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeFlaskBackEndwebhookAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeBackendEndpointscodereviewAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeBackendEndpointscodereviewAgent(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                                 index_,
#                                 login,
#                                 dashboard,
#                                 checkout,
#                                 checkout_sucess,
#                                 api_create_checkout,
#                                 api_register,
#                                 api_login,
#                                 webhook,



#                             )


#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeBackendEndpointscodereviewAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeBackendEndpointscodereviewAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }



#         def run_CodeFlaskBackEnd_basic_endpointsAgent(data, appcompany):
#             return asyncio.run(_CodeFlaskBackEnd_basic_endpointsAgent_logic(data, appcompany))

#         def run_CodeFlaskBackEndapi_create_checkoutAgent(data, appcompany):
#             return asyncio.run(_CodeFlaskBackEndapi_create_checkoutAgent_logic(data, appcompany))

#         def run_CodeFlaskBackEndapi_registerAgent(data, appcompany):
#             return asyncio.run(_CodeFlaskBackEndapi_registerAgent_logic(data, appcompany))

#         def run_CodeFlaskBackEndapi_loginAgent(data, appcompany):
#             return asyncio.run(_CodeFlaskBackEndapi_loginAgent_logic(data, appcompany))

#         def run_CodeFlaskBackEndwebhookAgent(data, appcompany):
#             return asyncio.run(_CodeFlaskBackEndwebhookAgent_logic(data, appcompany))

#         def run_CodeBackendEndpointscodereviewAgent(data, appcompany):
#             return asyncio.run(_CodeBackendEndpointscodereviewAgent_logic(data, appcompany))


#         results = []

#         try:
#             results.append(run_CodeFlaskBackEnd_basic_endpointsAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeFlaskBackEndapi_registerAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeFlaskBackEndapi_loginAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()
                
                
#         try:
#             results.append(run_CodeFlaskBackEndapi_create_checkoutAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#         try:
#             results.append(run_CodeFlaskBackEndwebhookAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()
                

#         try:
#             results.append(run_CodeBackendEndpointscodereviewAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()
                

#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201

# @app.route('/api/AgentsWorkFlow/Saas/teams/DevOps/Docker', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))  
# def api_AgentsWorkFlow_Saas_teams_DevOps():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     docker_file = data.get("docker_file")
#     docker_compose = data.get("docker_compose")
#     dockerbuild = data.get("dockerbuild")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")


#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():


#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }

#         async def _CodeDockerFileAgent_logic(data, appcompany):
#             session_id = data["session_id"]
#             user_email = data["user_email"]
#             agent, _ = CodeDockerFileAgent(session_id, appcompany,
#                                             path_ProjectWeb,
#                                             path_html,
#                                             path_js,
#                                             path_css,
#                                             doc_md,
#                                             Keys_path,
#                                             docker_file
#                                 )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["prompt_continuous"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "CodeDockerFileAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "CodeDockerFileAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeDockerComposeAgent_logic(data, appcompany):
#             session_id         = data["session_id"]
#             user_email         = data["user_email"]
#             prompt_continuous  = data.get("prompt_continuous", "")
#             agent, _ = CodeDockerComposeAgent(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                                 docker_compose
#                             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeDockerComposeAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeDockerComposeAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeDockerBuildAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeDockerBuildAgent(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                                 dockerbuild
#                             )
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeDockerBuildAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeDockerBuildAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeRequirementstxtAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeRequirementstxtAgent(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                             )
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeRequirementstxtAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeRequirementstxtAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeReview_DevOps_Docker_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeReview_DevOps_Docker(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                                 docker_file,
#                                 docker_compose,
#                                 dockerbuild
#                             )
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeReview_DevOps_Docker", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeReview_DevOps_Docker",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }



#         def run_CodeDockerFileAgent(data, appcompany):
#             return asyncio.run(_CodeDockerFileAgent_logic(data, appcompany))

#         def run_CodeDockerComposeAgent(data, appcompany):
#             return asyncio.run(_CodeDockerComposeAgent_logic(data, appcompany))

#         def run_CodeDockerBuildAgent(data, appcompany):
#             return asyncio.run(_CodeDockerBuildAgent_logic(data, appcompany))

#         def run_CodeRequirementstxtAgent(data, appcompany):
#             return asyncio.run(_CodeRequirementstxtAgent_logic(data, appcompany))

#         def run_CodeReview_DevOps_Docker(data, appcompany):
#             return asyncio.run(_CodeReview_DevOps_Docker_logic(data, appcompany))

#         results = []

#         try:
#             results.append(run_CodeDockerFileAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeDockerComposeAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()
                
#         try:
#             results.append(run_CodeDockerBuildAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeRequirementstxtAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#         try:
#             results.append(run_CodeReview_DevOps_Docker(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

        
#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201

# @app.route('/api/AgentsWorkFlow/Saas/teams/Documentation', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))  
# def api_AgentsWorkFlow_Saas_teams_Documentation():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")


#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }

#         async def _CodeDocumentationModulesAgent_logic(data, appcompany):
#             session_id = data["session_id"]
#             user_email = data["user_email"]
#             agent, _ = CodeDocumentationModulesAgent(
#                                     session_id, 
#                                     appcompany,
#                                     path_ProjectWeb,
#                                     path_html,
#                                     path_js,
#                                     path_css,
#                                     doc_md,
#                                     Keys_path,
#                                 )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["prompt_continuous"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "CodeDocumentationModulesAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "CodeDocumentationModulesAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeDocumentationStaticjsAgent_logic(data, appcompany):
#             session_id         = data["session_id"]
#             user_email         = data["user_email"]
#             prompt_continuous  = data.get("prompt_continuous", "")
#             agent, _ = CodeDocumentationStaticjsAgent(
#                                     session_id, 
#                                     appcompany,
#                                     path_ProjectWeb,
#                                     path_html,
#                                     path_js,
#                                     path_css,
#                                     doc_md,
#                                     Keys_path,
#                                 )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeDocumentationStaticjsAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeDocumentationStaticjsAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         async def _CodeDocumentationTechnichAgent_logic(data, appcompany):
#             session_id        = data["session_id"]
#             user_email        = data["user_email"]
#             prompt_continuous = data.get("prompt_continuous", "")
#             agent, _ = CodeDocumentationTechnichAgent(
#                                     session_id, 
#                                     appcompany,
#                                     path_ProjectWeb,
#                                     path_html,
#                                     path_js,
#                                     path_css,
#                                     doc_md,
#                                     Keys_path,
#                                 )
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "CodeDocumentationTechnichAgent", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "CodeDocumentationTechnichAgent",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }


#         def run_CodeDocumentationModulesAgent(data, appcompany):
#             return asyncio.run(_CodeDocumentationModulesAgent_logic(data, appcompany))

#         def run_CodeDocumentationStaticjsAgent(data, appcompany):
#             return asyncio.run(_CodeDocumentationStaticjsAgent_logic(data, appcompany))

#         def run_CodeDocumentationTechnichAgent(data, appcompany):
#             return asyncio.run(_CodeDocumentationTechnichAgent_logic(data, appcompany))

#         results = []

#         try:
#             results.append(run_CodeDocumentationModulesAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeDocumentationStaticjsAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#         try:
#             results.append(run_CodeDocumentationTechnichAgent(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201

# @app.route('/api/AgentsWorkFlow/Saas/teams/DevOps/RunBuild', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))  
# def api_AgentsWorkFlow_Saas_teams_DevOps_RunBuild():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")

#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         async def _RunBuildProject_logic(data, appcompany):
#             session_id = data["session_id"]
#             user_email = data["user_email"]
#             agent, _ = RunBuildProject(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                             )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["prompt_continuous"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "RunBuildProject", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "RunBuildProject",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         def run_RunBuildProject(data, appcompany):
#             return asyncio.run(_RunBuildProject_logic(data, appcompany))

#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }
#         results = []

#         try:
#             results.append(run_RunBuildProject(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201

# @app.route('/api/AgentsWorkFlow/Saas/teams/DevOps/EasyDeploy', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))  
# def api_AgentsWorkFlow_Saas_teams_DevOps_EasyDeploy():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")

#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         async def _DeployProjectModeEasy_logic(data, appcompany):
#             session_id         = data["session_id"]
#             user_email         = data["user_email"]
#             prompt_continuous  = data.get("prompt_continuous", "")

#             agent, _ = DeployProjectModeEasy(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                             )

#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         "info", agent, prompt_continuous,
#                         WEBHOOK_URL, session_id, user_email,
#                         "agent_", appcompany
#                     )
#                     return {"step": "DeployProjectModeEasy", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             return {
#                 "step": "DeployProjectModeEasy",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }

#         def run_DeployProjectModeEasy(data, appcompany):
#             return asyncio.run(_DeployProjectModeEasy_logic(data, appcompany))

#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }

#         results = []
#         try:
#             results.append(run_DeployProjectModeEasy(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()


#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201


# @app.route('/api/AgentsWorkFlow/Saas/teams/DevOps/UploadGit', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))
# def api_AgentsWorkFlow_Saas_teams_DevOps_UploadGit():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     private = data.get("private")
#     githubtoken = data.get("githubtoken")
#     repo_owner = data.get("repo_owner")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")


#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         data = {
#                 "session_id": session_id,
#                 "user_email": user_email,
#                 "prompt_continuous": prompt_continuous,
#             }

#         async def _CodeUploadGit_logic(data, appcompany):
#             session_id = data["session_id"]
#             user_email = data["user_email"]
#             agent, _ = CodeUploadGit(session_id, appcompany,
#                                 path_ProjectWeb,
#                                 path_html,
#                                 path_js,
#                                 path_css,
#                                 doc_md,
#                                 Keys_path,
#                                 githubtoken,
#                                 repo_owner,
#                                 private
#                             )

#             # retry + fallback
#             for _ in range(3):
#                 try:
#                     await process_stream(
#                         type_stream, agent, data["prompt_continuous"],
#                         WEBHOOK_URL, session_id, user_email, "1", appcompany
#                     )
#                     return {"step": "CodeUploadGit", "session_id": session_id}
#                 except Exception as e:
#                     if "Error streaming response" in str(e):
#                         continue
#                     raise

#             # se falhar 3 vezes, devolve com fallback
#             return {
#                 "step": "CodeUploadGit",
#                 "session_id": session_id,
#                 "fallback": "Erro de stream repetido"
#             }


#         def run_CodeUploadGit(data, appcompany):
#             return asyncio.run(_CodeUploadGit_logic(data, appcompany))

#         results = []

#         try:
#             results.append(run_CodeUploadGit(data, appcompany))
#         except Exception as e:
#             traceback.print_exc()

#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201






# @app.route('/api/AgentsWorkFlow/Saas/teams/QA', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))
# def api_AgentsWorkFlow_Saas_teams_QA():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     STRIPE_WEBHOOK_EVENTS = data.get("STRIPE_WEBHOOK_EVENTS")
#     STRIPE_SECRET_KEY = data.get("STRIPE_SECRET_KEY")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")


#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         os.chdir(path_ProjectWeb)
#         dotenv_path= os.path.join("Keys", "keys.env")
#         load_dotenv(dotenv_path=dotenv_path)
#         API_BASE_URL_Hosted_app = os.getenv("API_BASE_URL")
#         firebase_json_path = os.getenv("firebase_json_path")
#         firebase_db_url = os.getenv("firebase_db_url")

#         agent_unittest_user_created_by_ui, _ = unittest_user_created_by_ui("session_id", "appcompany",
#                             path_ProjectWeb,
#                             path_html,
#                             path_js,
#                             path_css,
#                             doc_md,
#                             Keys_path,
#                             STRIPE_WEBHOOK_EVENTS,
#                             STRIPE_SECRET_KEY,
#                             API_BASE_URL_Hosted_app,
#                             firebase_json_path,
#                             firebase_db_url,

#                         )

#         # # Run 1 agents 
#         # result = Runner.run_sync(agent_, prompt_continuous, max_turns=300)
#         # print(f"🤖 Resposta do sistema 14:\n{result.final_output}")


#         await process_stream_and_save_history(
#             type_stream,
#             agent_unittest_user_created_by_ui,
#             prompt_continuous,
#             WEBHOOK_URL,
#             session_id,
#             user_email,
#             "14",
#             appcompany
#             )


#         agent_unittest_login_user_by_ui, _ = unittest_login_user_by_ui("session_id", "appcompany",
#                             path_ProjectWeb,
#                             path_html,
#                             path_js,
#                             path_css,
#                             doc_md,
#                             Keys_path,
#                             STRIPE_WEBHOOK_EVENTS,
#                             STRIPE_SECRET_KEY,
#                             API_BASE_URL_Hosted_app,
#                             firebase_json_path,
#                             firebase_db_url,

#                         )
#         # # Run 1 agents 
#         # result = Runner.run_sync(agent_, prompt_continuous, max_turns=300)
#         # print(f"🤖 Resposta do sistema 15:\n{result.final_output}")

#         await process_stream_and_save_history(
#             type_stream,
#             agent_unittest_login_user_by_ui,
#             prompt_continuous,
#             WEBHOOK_URL,
#             session_id,
#             user_email,
#             "15",
#             appcompany
#             )


#         agent_unittest_user_checkout_by_ui, _ = unittest_user_checkout_by_ui("session_id", "appcompany",
#                             path_ProjectWeb,
#                             path_html,
#                             path_js,
#                             path_css,
#                             doc_md,
#                             Keys_path,
#                             STRIPE_WEBHOOK_EVENTS,
#                             STRIPE_SECRET_KEY,
#                             API_BASE_URL_Hosted_app,
#                             firebase_json_path,
#                             firebase_db_url,

#                         )
#         # # Run 1 agents 
#         # result = Runner.run_sync(agent_, prompt_continuous, max_turns=300)
#         # print(f"🤖 Resposta do sistema 16:\n{result.final_output}")


#         await process_stream_and_save_history(
#             type_stream,
#             agent_unittest_user_checkout_by_ui,
#             prompt_continuous,
#             WEBHOOK_URL,
#             session_id,
#             user_email,
#             "16",
#             appcompany
#             )


#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201

# @app.route('/api/AgentsWorkFlow/Saas/teams/ProductManager', methods=['POST'])
# @limiter.limit(lambda: dynamic_rate_limit(appcompany))
# def api_AgentsWorkFlow_Saas_teams_ProductManager():
#     data = request.get_json()
#     session_id = data.get("session_id")
#     user_email = data.get("user_email")
#     STRIPE_WEBHOOK_EVENTS = data.get("STRIPE_WEBHOOK_EVENTS")
#     STRIPE_SECRET_KEY = data.get("STRIPE_SECRET_KEY")
#     path_ProjectWeb = data.get("path_ProjectWeb")
#     path_html = data.get("path_html")
#     path_js = data.get("path_js")
#     path_css = data.get("path_css")
#     doc_md = data.get("doc_md")
#     path_Keys = data.get("path_Keys")
#     Keys_path = path_Keys
#     type_stream = data.get("type_stream")
#     prompt_continuous = data.get("prompt_continuous")


#     usuario, erro = autenticar_usuario(appcompany=appcompany)
#     if erro:
#         return erro

#     async def generate_response():

#         os.chdir(path_ProjectWeb)
#         dotenv_path= os.path.join("Keys", "keys.env")
#         load_dotenv(dotenv_path=dotenv_path)
#         API_BASE_URL_Hosted_app = os.getenv("API_BASE_URL")
#         firebase_json_path = os.getenv("firebase_json_path")
#         firebase_db_url = os.getenv("firebase_db_url")

#         agent_CreateProduct, _ = CreateProduct("session_id", "appcompany",
#                             path_ProjectWeb,
#                             path_html,
#                             path_js,
#                             path_css,
#                             doc_md,
#                             Keys_path,
#                             STRIPE_WEBHOOK_EVENTS,
#                             STRIPE_SECRET_KEY,
#                             API_BASE_URL_Hosted_app,
#                             firebase_json_path,
#                             firebase_db_url,

#                         )
#         # # Run 1 agents 
#         # result = Runner.run_sync(agent_, prompt_continuous, max_turns=300)
#         # print(f"🤖 Resposta do sistema 17:\n{result.final_output}")


#         await process_stream_and_save_history(
#             type_stream,
#             agent_CreateProduct,
#             prompt_continuous,
#             WEBHOOK_URL,
#             session_id,
#             user_email,
#             "17",
#             appcompany
#             )

#     def runner():
#         asyncio.run(generate_response())

#     threading.Thread(target=runner).start()
    
#     return jsonify({
#         "session_id": session_id,
#     }), 201




@app.route('/api/new-conversation', methods=['POST'])
def api_new_conversation():
    data = request.get_json()
    user_email = data.get("email")  # <- email deve vir do frontend

    if not user_email:
        return jsonify({"error": "Email é obrigatório"}), 400

    session_id = str(uuid.uuid4())
    user_email_filtred = user_email.replace(".", "_")
    logger.info(f"session_id {session_id}")
    now = datetime.utcnow().isoformat()

    ref = db.reference(f'users/{user_email_filtred}/conversations/{session_id}', app=appcompany)
    ref.set({
        "_meta": {
            "created_at": now
        }
    })

    return jsonify({
        "session_id": session_id,
        "snippet": "New Chat",
        "history": [],
        "timestamp": now
    }), 201

@app.route('/api/list-conversations', methods=['GET', 'POST'])
def list_conversations():
    user_email = request.args.get('user_email') or request.json.get('user_email')

    if not user_email:
        return jsonify({'error': 'Missing user_email'}), 400

    user_email_filtred = user_email.replace(".", "_")
    ref = db.reference(f'users/{user_email_filtred}/conversations', app=appcompany)
    user_conversations = ref.get()
    if not user_conversations:
        return jsonify([])

    all_convos = []
    for convo_id, convo_data in user_conversations.items():
        if not isinstance(convo_data, dict):
            continue

        messages = []
        title = "Nova conversa"
        created_at = None

        for k, v in convo_data.items():
            if k == "_meta":
                title = v.get("title", title)
                created_at = v.get("created_at", created_at)
            elif k.isdigit():
                messages.append(v)

        if not messages:
            continue  # ignora conversas vazias

        all_convos.append({
            "id": convo_id,
            "session_id": convo_id,
            "title": title,
            "created_at": created_at,
            "history": messages
        })

    all_convos.sort(key=lambda x: x.get("created_at", 0), reverse=True)
    return jsonify(all_convos)

@app.route('/api/check-session', methods=['GET'])
def check_session():
    logger.info(f"Sessão atual:{dict(session)}")  # <-- Adicione isso
    user_email = session["user"]
    user_data = db.reference(f'users/{user_email.replace(".", "_")}/github', app=appcompany).get()
    try:
        github_access_token = user_data.get("github_access_token")
        session['githubToken'] = github_access_token
        if 'user' in session:
            return jsonify({"logged_in": True, "email": session['user'], "githubToken": github_access_token})
    except:
        pass
    if 'user' in session:
        return jsonify({"logged_in": True, "email": session['user']})
    return jsonify({"logged_in": False})

@app.route('/api/save-settings', methods=['POST'])
def save_settings():
    data = request.get_json()
    email = data.get("email")
    logger.info("📥 Dados recebidos para salvar:", data)  # <--- ADICIONE ISSO

    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    email_safe = email.replace('.', '_')

    # Remove o email do dicionário antes de salvar
    settings_to_save = {k: v for k, v in data.items() if k != "email"}

    ref = db.reference(f'users/{email_safe}/settings/dashboard', app=appcompany)
    ref.set(settings_to_save)

    return jsonify({"message": "Configurações salvas com sucesso!"}), 200


@app.route('/api/load-settings', methods=['POST'])
def load_settings():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    email_safe = email.replace('.', '_')
    ref = db.reference(f'users/{email_safe}/settings/dashboard', app=appcompany)
    settings = ref.get()

    logger.info(f"📤 Dados carregados do Firebase:{settings}")

    return jsonify(settings), 200

@app.route('/api/load-apikey-and-limits', methods=['POST'])
def load_apikey_and_limits():
    data = request.get_json()
    email = data.get("email")

    if not email:
        return jsonify({"error": "Email é obrigatório"}), 400

    email_safe = email.replace('.', '_')
    ref = db.reference(f'users/{email_safe}', app=appcompany)
    settings = ref.get()

    logger.info("📤 Dados de API-and-Limits carregados do Firebase:", settings)
    
    return jsonify(settings), 200

@app.route("/create-checkout", methods=["POST"])
@limiter.limit(limit) 
def create_checkout():
    data = request.get_json()
    try:
        # Calcula a data de expiração: data atual + 31 dias
        expiration_time = datetime.now() + timedelta(days=31)
        SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_premium")

        session = stripe.checkout.Session.create(
            line_items=[{
                "price": SUBSCRIPTION_PRICE_ID,  # Usando o ID do preço definido no .env
                "quantity": 1
            }],
            mode="subscription",  # Modo de assinatura
            payment_method_types=["card"],
            success_url=f"{API_BASE_URL}/checkout/sucess",  # 
            cancel_url=f"{API_BASE_URL}/checkout/cancel",  # Caso o usuário cancele o pagamento
            metadata={"email": data["email"],
                      "password": data["password"],
                      "SUBSCRIPTION_PLAN": "premium",
                      "TIMESTAMP": expiration_time.isoformat()
                    },
        )
        logger.info(f"Sessão criada:{session.id}")
        return jsonify({"sessionId": session.id})
    except Exception as e:
        logger.info("Erro ao criar a sessão de checkout:", e)
        return jsonify({"error": str(e)}), 500


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
        return jsonify({"message": "Invalid payload"}), 400
    except stripe.error.SignatureVerificationError as e:
        logger.info("Assinatura inválida")
        return jsonify({"message": "Invalid signature"}), 400

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
            response = requests.post("https://softwareai.rshare.io/api/register", json=data, headers=headers)

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=829)

  # debug=True, 