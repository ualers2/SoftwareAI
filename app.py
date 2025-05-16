
# IMPORT SoftwareAI Libs
from softwareai_engine_library.Inicializer._init_libs_ import *
#########################################
from softwareai_engine_library.Chat._init_chat_ import *
#########################################
from softwareai_engine_library.EngineProcess.EgetMetadataAgent import *
#########################################
from softwareai_engine_library.EngineProcess.EgetTools import *
#########################################

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, supports_credentials=True, origins="*")

app.secret_key = 'sua_chave_secreta' 
app.permanent_session_lifetime = timedelta(days=7)  # exemplo: sessão dura 7 dias
app.config['SESSION_COOKIE_SECURE'] = False  # necessário em localhost
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'  # ou 'None' se for domínio cruzado

@app.context_processor
def inject_static_url():
    return dict(static_url=url_for('static', filename=''))

@app.route('/')
def index():
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
    return render_template('login_v2.html')

@app.route('/plan/prolight/checkout')
def plan_premium_checkout():
    return render_template('checkout/checkout.html')
 
@app.route('/checkout/sucess')
def checkoutsucess():
    return render_template('checkout/success.html')

@app.route('/checkout/cancel')
def checkoutcancel():
    return render_template('checkout/cancel.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=839)

  # debug=True, 