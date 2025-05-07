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
    print(f"Code Review FrontEnd JS Agent: {input_data.Content}")

def CodeReviewFrontEndJSAgent(session_id, appcompany):
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"templates"
    path_js = f"static/js"
    path_css = f"static/css"
    doc_md = f"doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

    Stripe_public_key = "pk_test_51QpX90Cvm2cRLHtdoF7n2Ea4sRRjYBx8Csiii0e6M6ECTJJ8fKaQ1DKpJApfJZH5hIkWRojaMmaxY9sEcS50tspB00DF2IA12h"

    checkout_payment_button = f"""

document.addEventListener("DOMContentLoaded", function() {{
  const urlParams = new URLSearchParams(window.location.search);
  const planParam = urlParams.get("plan");

  let plano;
  
  if (planParam === "free") {{
    window.location.href = `/login`;
  }} else {{
    plano = planParam;
  }}

  const payNowButton = document.querySelector('.block-pay-now .btn-primary');
  const loadingSpinner = document.querySelector('.loading-spinner');
  
  if (payNowButton) {{
    payNowButton.addEventListener("click", function() {{
      // Exibe o spinner de carregamento
      loadingSpinner.style.display = 'block';

      const selectedOption = document.querySelector('.option.selected');
      
      if (selectedOption) {{
        const paymentMethod = selectedOption.getAttribute("data-method");
        const email = document.querySelector('.email-input').value;
        const password = document.querySelector('.password-input').value;

        if (!email) {{
          alert("Por favor, insira seu email.");
          loadingSpinner.style.display = 'none';
          return; 
        }}

        fetch("/api/create-checkout", {{
          method: "POST",
          headers: {{
            "Content-Type": "application/json"
          }},
          body: JSON.stringify({{
            email: email,
            password: password,
            plano: plano          
          }}),
        }})
        .then(response => {{
          console.log("Resposta do servidor:", response);
          
          if (!response.ok) {{
            throw new Error("Erro na requisição. Status: " + response.status);
          }}
          return response.json()
            .catch(error => {{
              console.error("Erro ao converter a resposta para JSON:", error);
              throw new Error("Erro ao converter a resposta para JSON");
            }});
        }})
        .then(data => {{
          console.log("Dados recebidos:", data);
          loadingSpinner.style.display = 'none';
          
          if (data.sessionId) {{
            const stripe = Stripe("{Stripe_public_key}");
            stripe.redirectToCheckout({{ sessionId: data.sessionId }})
            .then(() => {{
              window.location.href = "/checkout/sucess";
            }});
          }} else {{
            alert("Erro ao criar a sessão de pagamento.");
          }}
        }})
        .catch(error => {{
          console.error("Erro ao enviar a requisição:", error);
          alert("Erro ao processar o pagamento.");
          loadingSpinner.style.display = 'none';
        }});
      }} else {{
        alert("Por favor, selecione um método de pagamento.");
        loadingSpinner.style.display = 'none';
      }}
    }});
  }}
}});


    """

    checkout_payment_selected = """
document.addEventListener("DOMContentLoaded", function() {
  const paymentOptions = document.querySelectorAll('.option');

  paymentOptions.forEach(function(option) {
    option.addEventListener("click", function() {
      // Remove a classe 'selected' de todas as opções
      paymentOptions.forEach(function(opt) {
        opt.classList.remove("selected");
      });
      
      // Adiciona a classe 'selected' na opção clicada
      option.classList.add("selected");
      
      // Loga o método de pagamento selecionado
      const selectedMethod = option.getAttribute("data-method");
      console.log("Método selecionado:", selectedMethod);
    });
  });
});

    """
    
    loginAndRegistrer = """
document.addEventListener("DOMContentLoaded", () => {
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
      input.type = 'text';
      toggleIcon.textContent = '🙈';
    } else {
      input.type = 'password';
      toggleIcon.textContent = '👁️';
    }
  };

  document.getElementById('login-btn').addEventListener('click', () => {
    const email = loginEmail.value.trim();
    const password = loginPassword.value;

    if (!email || !password) {
      return showMessage('Preencha todos os campos de login!');
    }

    showMessage('Carregando...', 'blue');
    fetch('/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      showMessage('Login realizado com sucesso!', 'green');
      localStorage.setItem('userEmail', email);
      localStorage.setItem('user_email', email);
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
    })
    .catch(err => showMessage('Erro de rede'));
  });

  document.getElementById('register-btn').addEventListener('click', () => {
    const name = registerName.value.trim();
    const email = registerEmail.value.trim();
    const password = registerPassword.value;

    if (!name || !email || !password) {
      return showMessage('Preencha todos os campos de cadastro!');
    }

    showMessage('Carregando...', 'blue');
    fetch('/api/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ name, email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      showMessage('Registro realizado com sucesso!', 'green');
      localStorage.setItem('userEmail', email);
      setTimeout(() => {
        window.location.href = '/dashboard';
      }, 1000);
    })
    .catch(err => showMessage('Erro de rede'));
  });
});

    """
    
    navigation_js = """

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


    """
    
    landing = """
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
          console.error(`Elemento destino '${targetSelector}' não encontrado.`);
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


    """
    

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