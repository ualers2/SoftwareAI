
![Screenshot_5](https://github.com/user-attachments/assets/10bc9339-c2d7-4933-876c-450fd65e2180)
<h1 align="center">SoftwareAI</h1>
<p align="center">None</p>

<p align="center"><code>npm i -g @ualers/softwareai-skeleton-engine</code></p>

![Codex demo GIF using: codex "explain this codebase to me"](./.github/demo.gif)

<details>
<summary><strong>Table of contents</strong></summary>

<!-- Begin ToC -->
- [Quickstart](#quickstart)
- [Why SoftwareAI?](#why-softwareai)
- [Requisitos do Sistema](#requisitos-do-sistema)
- [Referência da CLI](#referencia-da-cli)

<!-- End ToC -->

</details>

---

## Quickstart

Use o SoftwareAI em **3 passos simples**:

1. **Instale o CLI**

   ```bash
   npm install -g @ualers/softwareai-skeleton-engine
   ```

2. **Scaffold de um projeto Flask**

   ```bash
   create-py-app meu-projeto --theme flask-web-product
   ```

   * Gera o esqueleto em `./meu-projeto` com Docker, login, checkout e dashboard.

3. **Execute ou agende agentes**

   * Para rodar localmente:

     ```bash
     cd meu-projeto
     python app.py            # sem Docker
     # ou
     ```

docker-compose up --build # com Docker
\`\`\`

* Para agendar um agente:

  ```bash
  create-py-app schedule-task \
    --agent "AgentsWorkFlow.Saas.teams.ProjectManager" \
    --email "voce@exemplo.com" \
    --runAt "2025-05-20T15:30:00" \
    --repo "https://github.com/usuario/projeto.git" \
    --params '{"session_id":"xyz","user_message":"Olá"}'
  ```

---

## Por que Softwareai skeleton engine?

* 🚀 **Produtividade**: scaffolds e agendamentos prontos para usar.
* 🔄 **Integração**: funciona com Flask, Celery, Docker e Firebase.
* ⚙️ **Flexível**: crie templates próprios e escalone agentes via CLI.

---

## Requisitos do Sistema

* Node.js v14+
* Python 3.8+
* (Opcional) Docker & Docker Compose

---

## Referência da CLI

```bash
# Scaffold de projeto
create-py-app <nome-projeto> [--theme <tema>]

# Agendamento de agente
create-py-app schedule-task \
  --agent <nome> \
  --email <usuário> \
  --runAt <YYYY-MM-DDTHH:mm:ss> \
  --repo <URL_git> \
  [--params <JSON>]
```

---



# why-softwareai

#
#
# 📖 Library Web
- Provides a set of web services for listing, querying, and versioning agents and tools
- [Web Project Hosted](https://softwareai-library-hub.rshare.io)
- [Git Project](https://github.com/SoftwareAI-Company/SoftwareAI-Library-Web)
#
#
# 📖 Library Pip
- ```bash
  pip install softwareai-engine-library
  ```
- [Pip Project Hosted](https://pypi.org/project/softwareai-engine-library)
- [Git Project](https://github.com/SoftwareAI-Company/SoftwareAI-Library-Pip)
#
#
# 📖 SoftwareAI Chat
- Provides a web chat to utilize agents and tools from the SoftwareAI library.
- [Web Project Hosted](https://softwareai.rshare.io)
- [Git Project](https://github.com/SoftwareAI-Company/SoftwareAI-Chat)















