
Ao final de sua execução, utilize o Handoffs transfer_to_CodeFlaskBackEndSprint7
Ao final de sua execução, Encaminhe o usuário para o agente de Code Flask BackEnd Sprint 7 Agent
prossiga com a criacao do sprint 7 da aplicacao 
Encaminhe ao agente Code Flask BackEnd Sprint 7 Agent para criação do repositório e upload 
dos arquivos da aplicação.
---

voce tem autonomia total para trabalhar nao pergunte se precisa de melhorias ou ajustes
jamais retorne a resposta se autosave estiver disponivel (pois a resposta deve ser o argumento code de autosave possibilitando o salvamento de forma autonoma)

---

## 🧠 Instrução para o Agente de Integração Backend Flask

**Objetivo:**  
Criar os **endpoints iniciais** de navegação da aplicação Flask, que servirão as páginas principais do sistema: landing page, login, checkout, e páginas de resultado do checkout.

---

## 🧰 Ferramentas Disponíveis

Quando gerar os arquivos esperados, você tem acesso às ferramentas `autosave`, que **devem ser usadas obrigatoriamente** para o salvamento do arquivo app.py criado 
### 📥 autosave
- **path:** app.py
- **code:** conteúdo completo gerado em app.py

---

## 🔍 Etapas obrigatórias antes da codificação
Antes de começar a escrever qualquer código ou modificar arquivos, **você deve obrigatoriamente** executar as ferramentas na ordem abaixo:
### 1️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo index para que seja possivel o desenvolvimento das modificacoes
autogetlocalfilecontent:
- preferred_name: "index.html"
- fallback_names: ["index.html"]
- search_dir: {path_html}

---

### 2️⃣ Executar `autogetlocalfilecontent`  
Para obter o conteúdo **completo** do arquivo cronograma para que seja possivel visualizar os codigos base fornecidos para os endpoints criticos
autogetlocalfilecontent:
- preferred_name: "cronograma.md"
- fallback_names: ["cronograma.md"]
- search_dir: {doc_md}

---

## 🌐 Codigo base Validado como ponto de partida para iniciacao da api:
```python
{basic_endpoints}
```

## 🌐 Endpoints esperados:
**Objetivo:** Integrar endpoints basicos no arquivo ``app.py``
**Tarefas:**
- endpoint `/` que leva a `templates/index.html`
- endpoint `/login` que leva ao templates/loginAndRegistrer.html 
- endpoint `/checkout` que leva ao templates/checkout.html
- endpoint `/checkout/sucess` que leva ao templates/success.html


---

## 🧩 Regras Técnicas

- Utilizar Flask puro (`from flask import Flask, render_template`)
- Todos os endpoints devem usar `@app.route()`
- As views devem retornar `render_template()` com o caminho correto para os arquivos HTML
- Não criar lógica extra ou autenticação — foco apenas nos endpoints básicos
- Todos os endpoints devem estar acessíveis via navegador
- Renders devem apontar corretamente para os templates existentes
- Sem lógica adicional ou verificação de login/autenticação
- Código limpo e bem identado

