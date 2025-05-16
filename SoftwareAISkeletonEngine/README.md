# SoftwareAI Skeleton Engine

> **Transforme suas ideias em projetos Python prontos e agende agentes autônomos para executar tarefas programadas.**

**SoftwareAI Skeleton Engine** é um pacote que combina uma **CLI** e um **motor de orquestração** para:

* 🚀 **Programar Agentes para Trabalho**: agende agentes autônomos (via Flask/Celery) diretamente do terminal com o comando `schedule-task`.
* 📦 **Scaffold de Projetos**: crie esqueletos completos de aplicações Python (Flask) com templates pré-configurados e suporte a Docker.

---

## About

SoftwareAI é um framework cujo objetivo é permitir que uma organização governada por IA funcione como uma verdadeira empresa de desenvolvimento de software. Não se trata apenas de criar código: o SoftwareAI gerencia atualizações, documentação, agendamentos, planilhas e automatiza processos de toda a equipe.

---

## Funcionalidades Principais

| Comando         | Descrição                                                                                               |
| --------------- | ------------------------------------------------------------------------------------------------------- |
| `create-py-app` | Cria um novo projeto Flask com tema predefinido (`flask-web-product`).                                  |
| `schedule-task` | Programa um agente autônomo para execução futura, informando nome do agente, horário e repositório Git. |

---

## Esqueletos Disponíveis

* **flask-web-product**: Projeto Flask com telas de login, checkout Stripe, dashboard responsivo e Docker.

---

## Quickstart

### Pré-requisitos

* Node.js (v14+)
* NPM ou Yarn
* Python (v3.8+)
* (Opcional) Docker e Docker Compose

### Instalação

Instale o pacote globalmente usando NPM ou Yarn:

```bash
npm install -g @ualers/softwareai-skeleton-engine
# ou
yarn global add @ualers/softwareai-skeleton-engine
```

### Passo 1: Scaffold de Projeto

Gere um novo esqueleto Flask com Docker e funcionalidades prontas:

```bash
create-py-app meu-projeto --theme flask-web-product
```

Se nenhum tema for informado, o padrão `flask-web-product` será usado.

### Passo 2: Programando Agentes (schedule-task)

Com o servidor Flask/Celery rodando (endpoint `/schedule-agent`), use este comando para agendar um agente:

```bash
create-py-app schedule-task \
  --agent "AgentsWorkFlow.Saas.teams.ProjectManager" \
  --email "usuario@exemplo.com" \
  --runAt "2025-05-20T15:30:00" \
  --repo "https://github.com/usuario/projeto.git" \
  --params '{"session_id":"xyz","user_message":"Iniciar projeto"}'
```

Isso enviará o payload JSON:

```json
{
  "agent": "AgentsWorkFlow.Saas.teams.ProjectManager",
  "run_at": "2025-05-20T15:30:00-03:00",
  "repo_git": "https://github.com/usuario/projeto.git",
  "params": {
    "user_email": "usuario@exemplo.com",
    "session_id": "xyz",
    "user_message": "Iniciar projeto"
  }
}
```

## Freemium Product Landing

\[**Specialized AI Agents for Every Coding Task**]\([https://softwareai.rshare.io](https://softwareai.rshare.io))

Acelere seu fluxo de desenvolvimento com assistentes de IA treinados especificamente para:

* Documentação de código
* Refatoração e otimização
* Revisões e auditorias
* Geração de testes e exemplos

---

## Contribuição

1. Fork deste repositório
2. Crie uma branch: `git checkout -b feature/x`
3. Commit e push
4. Abra um Pull Request

---

## Licença

MIT
