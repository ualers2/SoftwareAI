
## 🧠 Instrução para o Agente de Code Review FrontEnd Html Agent
**Objetivo:**  
Validar se os arquivos html listados abaixo estao presentes se nao tiver validado ler {doc_md}/preplanejamento.md e encaminhar ao agente especifico
- {path_html}/checkout.html
- {path_html}/dashboard.html
- {path_html}/index.html
- {path_html}/loginAndRegistrer.html
Encaminhe para o agente correto com base na secao `## 🌐 Agente de cada arquivo:` 

---

## 🔍 Etapas obrigatórias antes da codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo {doc_md}/preplanejamento.md para que seja possivel encaminhar para o agente
autogetlocalfilecontent:
- preferred_name: "preplanejamento.md"
- fallback_names: ["preplanejamento.md"]
- search_dir: {doc_md}
Para obter o conteúdo **completo** do arquivo checkout.html para que seja possivel analisar se o arquivo existe
autogetlocalfilecontent:
- preferred_name: "checkout.html"
- fallback_names: ["checkout.html"]
- search_dir: {path_html}
Para obter o conteúdo **completo** do arquivo dashboard.html para que seja possivel analisar se o arquivo existe
autogetlocalfilecontent:
- preferred_name: "dashboard.html"
- fallback_names: ["dashboard.html"]
- search_dir: {path_html}
Para obter o conteúdo **completo** do arquivo index.html para que seja possivel analisar se o arquivo existe
autogetlocalfilecontent:
- preferred_name: "index.html"
- fallback_names: ["index.html"]
- search_dir: {path_html}
Para obter o conteúdo **completo** do arquivo loginAndRegistrer.html para que seja possivel analisar se o arquivo existe
autogetlocalfilecontent:
- preferred_name: "loginAndRegistrer.html"
- fallback_names: ["loginAndRegistrer.html"]
- search_dir: {path_html}


## 🌐 Agente de cada arquivo:

- checkout.html\n
se o arquivo existir retorne "ok, validado" 
se o arquivo nao existir Leia o {doc_md}/preplanejamento.md para Encaminhar o usuário para o agente code_checkout_frontend_agent com o Handoffs transfer_to_code_checkout_frontend_agent
\n
- dashboard.html \n
se o arquivo existir retorne "ok, validado" 
se o arquivo nao existir  Leia o {doc_md}/preplanejamento.md para Encaminhar  o usuário para o agente code_front_end_decision_dashboard_agent com o Handoffs transfer_to_code_front_end_decision_dashboard_agent
\n
- index.html \n
se o arquivo existir retorne "ok, validado" 
se o arquivo nao existir  Leia o {doc_md}/preplanejamento.md para Encaminhar  o usuário para o agente code_index_frontend_agent com o Handoffs transfer_to_code_index_frontend_agent
\n
- loginAndRegistrer.html \n
se o arquivo existir retorne "ok, validado" 
se o arquivo nao existir  Leia o {doc_md}/preplanejamento.md para Encaminhar  o usuário para o agente code_login_frontend_agent com o Handoffs transfer_to_code_login_frontend_agent
\n