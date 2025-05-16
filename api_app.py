
# IMPORT SoftwareAI Libs
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
from softwareai_engine_library.Chat._init_chat_ import *
#########################################
from softwareai_engine_library.EngineProcess.EgetMetadataAgent import *
#########################################
from softwareai_engine_library.EngineProcess.EgetTools import *
#########################################


dotenv_path = os.path.join(os.path.dirname(__file__), "Keys", "keys.env")
load_dotenv(dotenv_path=dotenv_path)

firebase_json_path = os.getenv("firebase_json_path")
firebase_db_url = os.getenv("firebase_db_url")



# --- Initialize Firebase ---
cred = credentials.Certificate(firebase_json_path)
appcompany = initialize_app(cred, {
    'databaseURL': firebase_db_url
},name="appcompany1")


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


@app.route('/api/AgentsWorkFlow/Saas', methods=['POST'])
@limiter.limit(lambda: dynamic_rate_limit(appcompany))
def api_AgentsWorkFlow_Saas():
    data = request.get_json()
    session_id = data.get("session_id")
    user_email = data.get("user_email")
    user_message = data.get("user_message")
    name_project = data.get("name_project")
    type_stream = "agentworkflow"

    usuario, erro = autenticar_usuario(appcompany=appcompany)
    if erro:
        return erro
    
    if not user_email:
        return jsonify({"error": "user_email is required"}), 400

    refuser = db.reference(f'users/{user_email.replace(".", "_")}', app=appcompany)
    data_user = refuser.get()
    refsettings = db.reference(f'users/{user_email.replace(".", "_")}/settings', app=appcompany)
    data_user_settings = refsettings.get()
    refdashboard = db.reference(f'users/{user_email.replace(".", "_")}/settings/dashboard', app=appcompany)
    data_user_dashboard = refdashboard.get()
    refgithub = db.reference(f'users/{user_email.replace(".", "_")}/settings/github', app=appcompany)
    data_user_github = refgithub.get()
    github_token = data_user_github.get("github_token")
    githubCompany = data_user_dashboard.get("githubCompany")
    STRIPE_SECRET_KEY = data_user_dashboard.get("STRIPE_SECRET_KEY")
    NEXT_PUBLIC_STRIPE_PUB_KEY = data_user_dashboard.get("NEXT_PUBLIC_STRIPE_PUB_KEY")
    STRIPE_WEBHOOK_EVENTS = "payout.paid customer.subscription.deleted checkout.session.async_payment_failed checkout.session.async_payment_succeeded checkout.session.expired checkout.session.completed checkout.session.expired invoice.payment_succeeded invoice.paid invoice.finalized invoice.updated payment_intent.created payment_intent.succeeded charge.succeeded"
    user_credentials_arg = data_user_settings.get("firebase_config")


    prompt_continuous = "Siga Com os objetivos da instrucao"
    path_ProjectWeb = f"/app/LocalProject/{name_project}"
    os.makedirs(path_ProjectWeb, exist_ok=True)
    os.chdir(path_ProjectWeb)
    path_html = f"templates"
    path_js = f"static/js"
    path_css = f"static/css"
    doc_md = f"doc_md"
    Keys_path = f"Keys"
    path_Keys = Keys_path
    githubtoken = github_token
    repo_owner = githubCompany
    user_credentials = user_credentials_arg
    os.makedirs(path_html, exist_ok=True)
    os.makedirs(path_js, exist_ok=True)
    os.makedirs(path_css, exist_ok=True)
    os.makedirs(doc_md, exist_ok=True)
    os.makedirs(Keys_path, exist_ok=True)
    
    os.chdir(os.path.join(os.path.dirname(__file__)))

    # Comando da CLI que foi instalada globalmente
    command = ["create-py-app", "--project", name_project]

    # Executar o comando no diretório do projeto
    try:
        result = subprocess.run(
            command,
            cwd=path_ProjectWeb,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        print("CLI output:", result.stdout)
    except subprocess.CalledProcessError as e:
        print("Erro ao rodar CLI:", e.stderr)
        return jsonify({"error": "Falha ao rodar create-py-app", "details": e.stderr}), 500

    async def generate_response():
        print("🧠 Enviando mensagem ao agente de triagem...")

        # /api/AgentsWorkFlow/Saas/teams/ProjectManager V

        # /api/AgentsWorkFlow/Saas/teams/FrontEnd V

        # /api/AgentsWorkFlow/Saas/teams/BackEnd V

        # /api/AgentsWorkFlow/Saas/teams/DevOps/Docker V

        # /api/AgentsWorkFlow/Saas/teams/Documentation V

        # /api/AgentsWorkFlow/Saas/teams/DevOps/RunBuild V

        # /api/AgentsWorkFlow/Saas/teams/DevOps/EasyDeploy V

        # /api/AgentsWorkFlow/Saas/teams/DevOps/UploadGit V

        # /api/AgentsWorkFlow/Saas/teams/QA 

        # /api/AgentsWorkFlow/Saas/teams/ProductManager


    # # Evita conflito de loops com interpretador
    # def run_async():
    #     try:
    #         loop = asyncio.new_event_loop()
    #         asyncio.set_event_loop(loop)
    #         loop.run_until_complete(generate_response())
    #     except Exception as e:
    #         print(f"Erro ao rodar stream do agente: {e}")


    # thread = threading.Thread(target=run_async, daemon=True)
    # thread.start()

    def runner():
        asyncio.run(generate_response())

    threading.Thread(target=runner).start()
    
    return jsonify({
        "session_id": session_id,
    }), 201


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
    app.run(host="0.0.0.0", port=859)

  # debug=True, 