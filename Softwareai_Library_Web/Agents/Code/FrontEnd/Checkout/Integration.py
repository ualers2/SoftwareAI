from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *

from Agents.Code.FrontEnd.NavigationJS.Integration import CodeNavigationJSFrontEnd

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeCheckoutFrontEnd: {input_data.FrontEndContent}")
    context_data = ctx.context or {}

    prompt_continuous = "Siga os Objetivos da instrucao"
    WEBHOOK_URL = context_data.get("WEBHOOK_URL")
    session_id = context_data.get("session_id")
    user_email = context_data.get("user_email")

    print(f"WEBHOOK_URL: {WEBHOOK_URL}")
    print(f"session_id: {session_id}")
    print(f"user_email: {user_email}")
    
              
def CodeCheckoutFrontEnd(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"templates"
    path_js = f"static/js"
    path_css = f"static/css"
    doc_md = f"doc_md"
    path_Keys = f"Keys"

    checkout_payment_button_js = """

document.addEventListener("DOMContentLoaded", function() {
  const urlParams = new URLSearchParams(window.location.search);
  const planParam = urlParams.get("plan");

  let plano;
  
  if (planParam === "free") {
    window.location.href = `/login`;
  } else {
    plano = planParam;
  }

  const payNowButton = document.querySelector('.block-pay-now .button');
  
  if (payNowButton) {
    payNowButton.addEventListener("click", function() {
      const selectedOption = document.querySelector('.option.selected');
      
      if (selectedOption) {
        const paymentMethod = selectedOption.getAttribute("data-method");
        const email = document.querySelector('.email-input').value;

        if (!email) {
          alert("Por favor, insira seu email.");
          return; 
        }

        fetch("/api/create-checkout", {
          method: "POST",
          headers: {
            "Content-Type": "application/json"
          },
          body: JSON.stringify({
            email: email,
            assinatura: true,
            plano: plano          
          }),
        })
        .then(response => {
          console.log("Resposta do servidor:", response);
        
          if (!response.ok) {
            throw new Error("Erro na requisição. Status: " + response.status);
          }
          return response.json()
            .catch(error => {
              console.error("Erro ao converter a resposta para JSON:", error);
              throw new Error("Erro ao converter a resposta para JSON");
            });
        })
        .then(data => {
          console.log("Dados recebidos:", data); 
        
          if (data.sessionId) {
            const stripe = Stripe("pk_test_51QpX90Cvm2cRLHtdoF7n2Ea4sRRjYBx8Csiii0e6M6ECTJJ8fKaQ1DKpJApfJZH5hIkWRojaMmaxY9sEcS50tspB00DF2IA12h");
            stripe.redirectToCheckout({ sessionId: data.sessionId })
            .then(() => {
              window.location.href = "/checkout/sucess"; 
            });
          } else {
            alert("Erro ao criar a sessão de pagamento.");
          }
        })
        .catch(error => {
          console.error("Erro ao enviar a requisição:", error);
          alert("Erro ao processar o pagamento.");
        });
      } else {
        // Caso nenhuma opção esteja selecionada, avise o usuário
        alert("Por favor, selecione um método de pagamento.");
      }
    });
  }
});

    """
    
    checkout_payment_selected_js = """
document.addEventListener("DOMContentLoaded", function() {
    const paymentOptions = document.querySelectorAll('.option');
  
    paymentOptions.forEach(function(option) {
      option.addEventListener("click", function() {
        paymentOptions.forEach(function(opt) {
          opt.classList.remove("selected");
        });
        option.classList.add("selected");
        const selectedMethod = option.getAttribute("data-method");
        console.log("Método selecionado:", selectedMethod);
      });
    });
  });
  
    """

    session_id_CodeNavigationJSFrontEnd = "teste_handoff_CodeNavigationJSFrontEnd"
    agent_, handoff_obj_CodeNavigationJSFrontEnd = CodeNavigationJSFrontEnd(session_id_CodeNavigationJSFrontEnd, appcompany)
# ---
# ## 🧰 Ferramentas Disponíveis

# Quando gerar os arquivos esperados, você tem acesso às ferramentas `autosave`, que **devem ser usadas obrigatoriamente** para o salvamento do arquivo criado (se houver mais de um arquivo use a ferramenta uma vez para cada arquivo)
# ### 📥 autosave
# - **path:** localizacao esperada do arquivo
# - **code:** conteúdo completo gerado


# ### 📥 `autoupload`  
#   - repo_name: nome do projeto armazenado no historico de conversas
#   - repo_owner: {repo_owner}  
#   - softwarepypath: {path_html}/checkout.html e {path_js}/checkout-payment-button.js (no caso de 2 arquivos utilize a ferramenta 1 vez para cada arquivo)
#   - token: {githubtoken}


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
        handoffs=[handoff_obj_CodeNavigationJSFrontEnd],

    )


    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
    )
    return agent, handoff_obj