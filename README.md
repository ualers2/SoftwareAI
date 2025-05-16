<h1 align="center">SoftwareAI</h1>

![Screenshot_5](https://github.com/user-attachments/assets/10bc9339-c2d7-4933-876c-450fd65e2180)

<p align="center">It's not just about writing code: SoftwareAI manages updates, documentation, schedules, spreadsheets, and automates processes for the entire team</p>

<p align="center"><code>npm i -g @ualers/softwareai-skeleton-engine</code></p>

<details>
<summary><strong>Table of contents</strong></summary>

<!-- Begin ToC -->
- [Quickstart](#quickstart)
- [Why SoftwareAI?](#why-softwareai)
- [System Requirements](#system-requirements)
- [CLI Reference](#cli-reference)
<!-- End ToC -->

</details>

---

## Quickstart
Use SoftwareAI in **3 easy steps**:

1. **Install the CLI**

```bash
npm install -g @ualers/softwareai-skeleton-engine
```

2. **Scaffold a Flask project**

```bash
create-py-app my-project --theme flask-web-product
```

* Generates the skeleton in `./my-project` with Docker, login, checkout and dashboard.

3. **Run or schedule agents**

* To run locally:

```bash
cd my-project
python app.py # without Docker
# or
```

docker-compose up --build # with Docker
\`\`\`

* To schedule an agent:

```bash
create-py-app schedule-task \
--agent "AgentsWorkFlow.Saas.teams.ProjectManager" \
--email "you@example.com" \
--runAt "2025-05-20T15:30:00" \
--repo "https://github.com/user/project.git" \
--params '{"session_id":"xyz","user_message":"Hello"}'
```
---
## Why Softwareai skeleton engine?

* 🚀 **Productivity**: ready-to-use scaffolds and scheduling.
* 🔄 **Integration**: works with Flask, Celery, Docker and Firebase.
* ⚙️ **Flexible**: create your own templates and schedule agents via CLI.

---

## System Requirements

* Node.js v14+
* Python 3.8+
* (Optional) Docker & Docker Compose

---

## CLI Reference

```bash
  # Project Scaffolding
  create-py-app <project-name> [--theme <theme>]

  # Agent Scheduling
  create-py-app schedule-task \
  --agent <name> \
  --email <user> \
  --runAt <YYYY-MM-DDTHH:mm:ss> \
  --repo <git_URL> \
  [--params <JSON>]
```

---

# why-softwareai

SoftwareAI is a framework that aims to enable an AI-driven organization to function like a real software development company. It's not just about writing code: SoftwareAI manages updates, documentation, schedules, spreadsheets, and automates processes for the entire team. 

#
#
# 📖 Library Web
- Provides a set of web services for listing, querying, and versioning agents and tools
- [Web Project Hosted](https://softwareai-library-hub.rshare.io)
- [Git Project](https://github.com/SoftwareAI-Company/SoftwareAI-Library-Web)
#
#
# 📖Library Pip
- ```bash
  pip install softwareai-engine-library
  ```
- [Git Project](https://github.com/SoftwareAI-Company/SoftwareAI-Library-Pip)
#
#
# 📖 SoftwareAI Chat
- Provides a web chat to use agents and tools from the SoftwareAI library.
- [Web Project Hosted](https://softwareai.rshare.io)
- [Git Project](https://github.com/SoftwareAI-Company/SoftwareAI-Chat)












