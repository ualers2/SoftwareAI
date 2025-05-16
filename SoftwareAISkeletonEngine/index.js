
import { program } from 'commander';
import inquirer from 'inquirer';
import fs from 'fs-extra';
import path from 'path';

const appPy= `import os
import sys
import json
import uuid
import secrets
from datetime import timedelta, datetime

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

import stripe
import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import logging

from dotenv import load_dotenv
from firebase_admin import db
from Keys.fb import init_firebase

# Change current working directory to the file's directory
os.chdir(os.path.join(os.path.dirname(__file__)))

# Criação da aplicação Flask
app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app, supports_credentials=True, origins="*")

# Configurações de sessão
app.secret_key = 'sua_chave_secreta'
app.permanent_session_lifetime = timedelta(days=7)
app.config['SESSION_COOKIE_SECURE'] = False
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

# Integração de Código Base para Firebase, dotenv e Stripe
app_instance = init_firebase()
load_dotenv(dotenv_path="Keys/keys.env")

gmail_usuario = os.getenv("gmail_usuario")
gmail_senha = os.getenv("gmail_senha")
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET")
SUBSCRIPTION_PRICE_ID = os.getenv("STRIPE_SUBSCRIPTION_PRICE_ID_premium")
API_BASE_URL = os.getenv("API_BASE_URL")

# logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Limiter config

def get_api_key():
    return request.headers.get('X-API-KEY')


def key_func():
    api_key = get_api_key()
    return api_key if api_key else get_remote_address()


def generate_api_key(subscription_plan):
    prefix_map = {
        "premium": "apikey-premium",
    }
    prefix = prefix_map[subscription_plan.lower()] 
    unique_part = secrets.token_urlsafe(32)
    return f"{prefix}-{unique_part}"

limiter = Limiter(app=app, key_func=key_func, default_limits=["10 per minute"])

# Rotas Principais
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/checkout')
def checkout():
    plan_name = request.args.get('plan', 'free')
    return render_template('checkout.html', plan=plan_name)

@app.route('/checkout/sucess')
def checkout_sucess():
    return render_template('success.html')


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


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
`;

const checkoutPaymentButton = `document.addEventListener("DOMContentLoaded", function() {
  const urlParams = new URLSearchParams(window.location.search);
  const planParam = urlParams.get("plan");
  let plano;

  if (planParam === "free") {
    window.location.href = "/login";
  } else {
    plano = planParam;
  }

  const payNowButton = document.querySelector('.block-pay-now .btn-primary');
  const loadingSpinner = document.querySelector('.loading-spinner');

  if (payNowButton) {
    payNowButton.addEventListener("click", function() {
      loadingSpinner.style.display = 'block';
      const selectedOption = document.querySelector('.option.selected');
      if (selectedOption) {
        const email = document.querySelector('.email-input').value;
        const password = document.querySelector('.password-input').value;
        if (!email) {
          alert("Por favor, insira seu email.");
          loadingSpinner.style.display = 'none';
          return;
        }
        fetch("/api/create-checkout", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email, password, plano })
        })
        .then(response => {
          if (!response.ok) throw new Error("Status: " + response.status);
          return response.json();
        })
        .then(data => {
          loadingSpinner.style.display = 'none';
          if (data.sessionId) {
            const stripe = Stripe(process.env.NEXT_PUBLIC_STRIPE_PUB_KEY);
            stripe.redirectToCheckout({ sessionId: data.sessionId })
              .then(() => window.location.href = "/checkout/sucess");
          } else alert("Erro ao criar a sessão de pagamento.");
        })
        .catch(err => {
          alert("Erro ao processar o pagamento.");
          loadingSpinner.style.display = 'none';
        });
      } else {
        alert("Por favor, selecione um método de pagamento.");
        loadingSpinner.style.display = 'none';
      }
    });
  }
});`;

const checkoutPaymentSelected = `document.addEventListener("DOMContentLoaded", function() {
  const paymentOptions = document.querySelectorAll('.option');
  paymentOptions.forEach(function(option) {
    option.addEventListener("click", function() {
      paymentOptions.forEach(opt => opt.classList.remove("selected"));
      option.classList.add("selected");
      console.log("Método selecionado:", option.getAttribute("data-method"));
    });
  });
});`;

const loginAndRegister = `document.addEventListener("DOMContentLoaded", () => {
  const msg = document.getElementById('msg');
  const loginEmail = document.getElementById('login-email');
  const loginPassword = document.getElementById('login-password');
  const registerName = document.getElementById('register-name');
  const registerEmail = document.getElementById('register-email');
  const registerPassword = document.getElementById('register-password');

  function showMessage(text, color = "red") {
    msg.textContent = text;
    msg.style.color = color;
  }

  window.toggleForms = function() {
    const loginForm = document.getElementById('login-form');
    const registerForm = document.getElementById('register-form');
    if (loginForm.style.display === 'none') {
      loginForm.style.display = 'block';
      registerForm.style.display = 'none';
    } else {
      loginForm.style.display = 'none';
      registerForm.style.display = 'block';
    }
    showMessage("");
  };

  window.togglePassword = function(inputId, toggleIcon) {
    const input = document.getElementById(inputId);
    if (input.type === 'password') {
      input.type = 'text'; toggleIcon.textContent = '🙈';
    } else {
      input.type = 'password'; toggleIcon.textContent = '👁️';
    }
  };

  document.getElementById('login-btn').addEventListener('click', () => {
    const email = loginEmail.value.trim();
    const password = loginPassword.value;
    if (!email || !password) return showMessage('Preencha todos os campos de login!');
    showMessage('Carregando...', 'blue');
    fetch('/api/login', {
      method: 'POST', headers: {'Content-Type':'application/json'}, credentials:'include',
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      showMessage('Login realizado com sucesso!', 'green');
      localStorage.setItem('userEmail', email);
      setTimeout(() => window.location.href='/dashboard', 1000);
    }).catch(() => showMessage('Erro de rede'));
  });

  document.getElementById('register-btn').addEventListener('click', () => {
    const name = registerName.value.trim();
    const email = registerEmail.value.trim();
    const password = registerPassword.value;
    if (!name || !email || !password) return showMessage('Preencha todos os campos de cadastro!');
    showMessage('Carregando...', 'blue');
    fetch('/api/register', {
      method: 'POST', headers:{'Content-Type':'application/json'},
      body: JSON.stringify({ name, email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      showMessage('Registro realizado com sucesso!', 'green');
      localStorage.setItem('userEmail', email);
      setTimeout(() => window.location.href='/dashboard', 1000);
    }).catch(() => showMessage('Erro de rede'));
  });
});`;

const navigation_js = `

/* navigation.js - Gerencia a navegação via cliques, especificamente para os botões de planos. */

document.addEventListener('DOMContentLoaded', () => {
// Seleciona os botões de planos
const basicPlanBtn = document.getElementById('plan-basic');
const premiumPlanBtn = document.getElementById('plan-premium');

if (!basicPlanBtn) {
    console.error('Botão do plano Básico não encontrado. Verifique o ID plan-basic.');
} else {
    basicPlanBtn.addEventListener('click', () => {
    // Redireciona para a página de login para o plano gratuito
    window.location.href = '/login';
    });
}

if (!premiumPlanBtn) {
    console.error('Botão do plano Premium não encontrado. Verifique o ID plan-premium.');
} else {
    premiumPlanBtn.addEventListener('click', () => {
    // Redireciona para a página de checkout com parâmetro do plano premium
    window.location.href = '/checkout?plan=premium';
    });
}
});


`;
const landing_js = `
/* landing.js - Refatoração do código inline presente no index.html para melhorar a modularidade e a organização do JavaScript da landing page. */

document.addEventListener('DOMContentLoaded', () => {
  // Função para manipulação do menu mobile
  function initMobileMenu() {
    const menuToggle = document.getElementById('mobile-menu');
    const navLinks = document.getElementById('nav-links');
    if (!menuToggle || !navLinks) {
      console.error('Elementos do menu mobile não encontrados.');
      return;
    }
    menuToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }

  // Função para scroll suave ao clicar nos links do menu
  function initSmoothScrolling() {
    const navAnchors = document.querySelectorAll('.nav-links a');
    const navLinks = document.getElementById('nav-links');

    navAnchors.forEach(anchor => {
      anchor.addEventListener('click', function(e) {
        e.preventDefault();
        const targetSelector = this.getAttribute('href');
        const targetElement = document.querySelector(targetSelector);
        if (targetElement) {
          targetElement.scrollIntoView({ behavior: 'smooth' });
        } else {
          console.error(\`Elemento destino \${targetSelector} não encontrado.\`);
        }
        if (navLinks && navLinks.classList.contains('active')) {
          navLinks.classList.remove('active');
        }
      });
    });
  }

  // Função para o comportamento de acordeão na seção FAQ
  function initFAQAccordion() {
    const faqItems = document.querySelectorAll('.faq-item');
    if (!faqItems.length) {
      console.error('Nenhum item de FAQ encontrado.');
      return;
    }
    faqItems.forEach(item => {
      item.addEventListener('click', () => {
        item.classList.toggle('active');
      });
    });
  }

  // Função para o slider de depoimentos
  function initTestimonialSlider() {
    const testimonials = document.querySelectorAll('.testimonial');
    const controlsContainer = document.getElementById('slider-controls');
    if (!testimonials.length || !controlsContainer) {
      console.error('Depoimentos ou controles do slider não encontrados.');
      return;
    }
    const controls = controlsContainer.children;
    let currentTestimonial = 0;

    function showTestimonial(index) {
      testimonials.forEach((testimonial, i) => {
        testimonial.style.display = (i === index) ? 'block' : 'none';
      });
      Array.from(controls).forEach(control => control.classList.remove('active'));
      if (controls[index]) controls[index].classList.add('active');
    }

    showTestimonial(currentTestimonial);

    Array.from(controls).forEach(control => {
      control.addEventListener('click', (e) => {
        const index = parseInt(e.target.getAttribute('data-index'));
        if (!isNaN(index)) {
          currentTestimonial = index;
          showTestimonial(currentTestimonial);
        } else {
          console.error('Índice inválido para o slider de depoimentos.');
        }
      });
    });

    // Auto slide a cada 5 segundos
    setInterval(() => {
      currentTestimonial = (currentTestimonial + 1) % testimonials.length;
      showTestimonial(currentTestimonial);
    }, 5000);
  }

  // Inicializa todas as funções
  initMobileMenu();
  initSmoothScrolling();
  initFAQAccordion();
  initTestimonialSlider();
});
`;

const script_base_login_js = `
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const msg = document.getElementById('msg');

function showMessage(text, color = "red") {
  msg.textContent = text;
  msg.className = \`text-sm text-center text-\${color}-400\`;
}

document.addEventListener("DOMContentLoaded", () => {
  document.getElementById('login-btn').addEventListener('click', () => {
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const api_url_login = "/api/login";
    
    fetch(api_url_login, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      
      showMessage("Login realizado com sucesso!", "green");

      localStorage.setItem("userEmail", email);
      localStorage.setItem("user_email", email);

      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
    })
    .catch(err => showMessage("Erro de rede"));
  });

  document.getElementById('register-btn').addEventListener('click', () => {
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const api_url_register = "/api/register";

    fetch(api_url_register, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      
      showMessage("Registro realizado com sucesso!", "green");

      localStorage.setItem("userEmail", email);

      setTimeout(() => {
        window.location.href = "/dashboard";
      }, 1000);
    })
    .catch(err => showMessage("Erro de rede"));
  });
});
`;
const user_code_init_env = `
STRIPE_WEBHOOK_SECRET=
STRIPE_SECRET_KEY={STRIPE_SECRET_KEY}
STRIPE_SUBSCRIPTION_PRICE_ID_Premium=
NEXT_PUBLIC_STRIPE_PUB_KEY={NEXT_PUBLIC_STRIPE_PUB_KEY}
gmail_usuario=
gmail_senha=
API_BASE_URL="http://127.0.0.1:5000"

firebase_json_path=
firebase_db_url=
`;

const docker_file = `
FROM python:3.12-slim
RUN apt-get update && \
    apt-get install -y \
    git

# Install Node.js 22.x (needed for codex CLI)
RUN apt-get update && \
    apt-get install -y curl gnupg ca-certificates && \
    curl -fsSL https://deb.nodesource.com/setup_22.x | bash - && \
    apt-get install -y nodejs && \
    rm -rf /var/lib/apt/lists/*

# Install codex CLI globally
RUN npm install -g @openai/codex

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

RUN git init /app

# Copiar todos os arquivos do projeto
COPY . /app


`;

const docker_compose_file = `
version: '3.8'

services:
  landingpage:
    build: .
    container_name: landingpageapp
    restart: always
    ports:
      - "5000:5000"
    volumes:
      - .:/app
      - /var/run/docker.sock:/var/run/docker.sock
    command: >
      sh -c "python app.py"
    mem_limit: 500MB
    cpus: "1.5"

`;

const repo_file = `
{"name": "", "remotegit": ""}
`;

const appcompany_file = `
`;

const fb_file = `

from firebase_admin import initialize_app, credentials
import os
from dotenv import load_dotenv, find_dotenv

def init_firebase():
    dotenv_path= os.path.join(os.path.dirname(__file__), "keys.env")
    load_dotenv(dotenv_path=dotenv_path)
    firebase_json_path = os.getenv("firebase_json_path")
    firebase_db_url = os.getenv("firebase_db_url")
    cred = credentials.Certificate(firebase_json_path)
    app = initialize_app(cred, {
        'databaseURL': firebase_db_url
    })
    return app


    
`;

const requirements_file = `
Flask
Flask-Cors
Flask-Limiter
stripe
requests
python-dotenv
firebase-admin
`;

const build_file = `
import subprocess
import os

# Define o diretório de trabalho como o diretório do arquivo atual
os.chdir(os.path.join(os.path.dirname(__file__)))

# Adiciona o caminho do Docker Compose ao PATH do sistema
os.environ["PATH"] += r";C:\Program Files\Docker\Docker\resources\bin"


def executar_comando(comando):
    """Executa um comando sem abrir um novo terminal (funciona dentro do contêiner)."""
    subprocess.run(comando, shell=True)


# Executa o comando do docker-compose para build e subir os containers
executar_comando("docker-compose up --build")

`;





// Templates mapping
const themes = {
  'flask-web-product': {
    description: 'Flask web product with Checkout, Login, Dashboard',
    files: [
      { target: 'app.py', content: appPy},
      { target: 'Dockerfile', content: docker_file},
      { target: 'docker-compose.yml', content: docker_compose_file},
      { target: 'repo.json', content: repo_file},
      { target: 'build.py', content: build_file},
      { target: 'requirements.txt', content: requirements_file},
      { target: 'static/js/checkout-payment-button.js', content: checkoutPaymentButton },
      { target: 'static/js/checkout-payment-selected.js', content: checkoutPaymentSelected },
      { target: 'static/js/loginAndRegistrer.js', content: loginAndRegister },
      { target: 'static/js/navigation.js', content: navigation_js},
      { target: 'static/js/landing.js', content: landing_js},
      { target: 'Keys/keys.env', content: user_code_init_env},
      { target: 'Keys/appcompany.json', content: appcompany_file},
      { target: 'Keys/fb.py', content: fb_file},
    ],
    placeholders: ['index','login','dashboard','checkout','success']
  }
};

async function main() {
  program
    .name('create-py-app')
    .description('Scaffold Flask Python app with multiple themes')
    .version('1.2.0')
    .option('-t, --theme <theme>', 'Choose an application theme', 'flask-web-product');

  program
    .argument('<project-name>', 'Project folder name')
    .action(async (name, options) => {
      const { theme } = options;
      if (!themes[theme]) {
        console.error(`Unknown theme '${theme}'. Available: ${Object.keys(themes).join(', ')}`);
        process.exit(1);
      }

      const root = path.resolve(process.cwd(), name);
      if (await fs.pathExists(root)) {
        console.error(`Directory ${name} exists.`);
        process.exit(1);
      }

      // Create directories
      await fs.mkdirp(root);
      await fs.mkdirp(path.join(root, 'templates'));
      await fs.mkdirp(path.join(root, 'static/js'));
      await fs.mkdirp(path.join(root, 'static/css'));
      await fs.mkdirp(path.join(root, 'Keys'));

      const themeDef = themes[theme];

      // Write theme files
      for (const file of themeDef.files) {
        const targetPath = path.join(root, file.target);
        await fs.mkdirp(path.dirname(targetPath));
        await fs.writeFile(targetPath, file.content);
      }

      // Write placeholders
      themeDef.placeholders.forEach(page => {
        const tpl = path.join(root, 'templates', `${page}.html`);
        fs.writeFileSync(tpl, `<!-- ${page} for theme ${theme} -->`);
      });

      // Write README
      const readme = `# ${name}

Created with theme '${theme}': ${themeDef.description}
`;
      await fs.writeFile(path.join(root, 'README.md'), readme);

      console.log(`Project '${name}' created using theme '${theme}'.`);
    });

  await program.parseAsync();
}


main();
