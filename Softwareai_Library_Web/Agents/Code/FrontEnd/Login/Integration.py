from agents import Agent, handoff, RunContextWrapper
import requests
from dotenv import load_dotenv, find_dotenv
import os
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX
from pydantic import BaseModel
from modules.modules import *

from Agents.Code.FrontEnd.Checkout.Integration import CodeCheckoutFrontEnd

class FrontEndData(BaseModel):
    FrontEndContent: str

async def on_handoff(ctx: RunContextWrapper[dict], input_data: FrontEndData):
    print(f"CodeIndexFrontEnd: {input_data.FrontEndContent}")
    # response = requests.post("http://localhost:5000/agent/refund", json={"input": input_data.reason})
    # reply = response.json().get("reply")
              
def CodeLoginFrontEnd(session_id, appcompany):
   
    path_ProjectWeb = "/app/LocalProject"
    os.chdir(path_ProjectWeb)
    path_html = f"{path_ProjectWeb}/templates"
    path_js = f"{path_ProjectWeb}/static/js"
    path_css = f"{path_ProjectWeb}/static/css"
    doc_md = f"{path_ProjectWeb}/doc_md"

    githubtoken = os.getenv("github_username_Ualers")
    repo_owner = os.getenv("companyname")

    session_id_CodeCheckoutFrontEnd = "teste_handoff_CodeCheckoutFrontEnd"
    agent_, handoff_obj_CodeCheckoutFrontEnd = CodeCheckoutFrontEnd(session_id_CodeCheckoutFrontEnd, appcompany)
    
    script_base_login_js = '''
const emailInput = document.getElementById('email');
const passwordInput = document.getElementById('password');
const msg = document.getElementById('msg');

function showMessage(text, color = "red") {
  msg.textContent = text;
  msg.className = `text-sm text-center text-${{color}}-400`;
}
document.addEventListener("DOMContentLoaded", () => {
  document.getElementById('login-btn').addEventListener('click', () => {
    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const api_url_login = "/api/login";
    fetch(api_url_login, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',  // 👈 necessário para manter a sessã
      body: JSON.stringify({ email, password })
    })
    .then(res => res.json())
    .then(data => {
      if (data.error) return showMessage(data.error);
      
      showMessage("Login realizado com sucesso!", "green");

      // ✅ Armazena email para uso futuro se quiser
      localStorage.setItem("userEmail", email);
      localStorage.setItem("user_email", email);
      
      // ✅ Redireciona após login, se necessário
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
    
        // ✅ Armazena email para uso futuro se quiser
        localStorage.setItem("userEmail", email);
    
        // ✅ Redireciona após login, se necessário
        setTimeout(() => {
          window.location.href = "/dashboard";
        }, 1000);
      })
      .catch(err => showMessage("Erro de rede"));
  });
});

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
        handoffs=[handoff_obj_CodeCheckoutFrontEnd],


    )

    handoff_obj = handoff(
        agent=agent,
        on_handoff=on_handoff,
        input_type=FrontEndData,
        tool_name_override="code_login_front_end_agent"
    )
    return agent, handoff_obj