
## 🧠 Instrução para o Agente de Back end endpoints code review 
**Objetivo:**  
Validar se o **app.py** com contem os endpoints base listados abaixo
 
- /
- /login
- /dashboard
- /checkout
- /checkout/sucess
- /api/create-checkout
- /api/register 
- /api/login
- /webhook

se Validado tiver retorne "ok, validado" 
se Validado nao tiver refatore o arquivo no endpoint faltante com base na secao `## 🌐 Codigo Base de cada Endpoint:` e retorne "ok, refatorado"  
---



## 🔍 Etapas obrigatórias antes da codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo app.py para que seja possivel analisar se há endpoints faltantes
autogetlocalfilecontent:
- preferred_name: "app.py"
- fallback_names: ["app.py"]
- search_dir: {path_ProjectWeb}

---
## 🧰 Ferramentas Disponíveis
Caso algum dos endpoints nao forem validados, você tem acesso às ferramentas `autosave`, que **devem ser usadas obrigatoriamente** para o salvamento do arquivo app.py criado 
### 📥 autosave
- **path:** app.py
- **code:** conteúdo completo gerado em app.py

---

## 🌐 Codigo Base de cada Endpoint:

- / \n
{index_}\n

- /login\n
{login}\n

- /dashboard\n
{dashboard}\n

- /checkout\n
{checkout}\n

- /checkout/sucess\n
{checkout_sucess}\n

- /api/create-checkout\n
{api_create_checkout}\n

- /api/register\n
{api_register}\n

- /api/login\n
{api_login}\n

- /webhook\n
{webhook}\n



---