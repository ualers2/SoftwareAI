# SoftwareAI Skeleton Engine

**Transforme suas ideias em projetos Python prontos e agende agentes automaticamente, economizando tempo e recursos.**

Este pacote atua como uma **CLI** e **engine** para:

* **Escalonamento de Agentes**: Agende execuções programadas de agentes (via Flask/Celery) diretamente do terminal.
* **Scaffold de Projetos**: Crie esqueletos completos de aplicações Python (Flask) com templates e containers Docker.

## Funcionalidades Principais

| Comando         | Descrição                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------- |
| `create-py-app` | Cria um novo projeto Flask com tema predefinido (`flask-web-product`).                       |
| `schedule-task` | Agenda um agente para execução futura, informando nome do agente, horário e repositório Git. |

## Esqueletos Disponíveis

* **flask-web-product**: Projeto Flask com telas de login, checkout Stripe, dashboard e Docker.

## Quickstart

### Pré-requisitos

* Node.js (v14+)
* NPM ou Yarn
* Python (v3.8+)
* (Opcional) Docker e Docker Compose

### Instalação

Via NPM:

```bash
npm install -g @ualers/softwareai-skeleton-engine
```

Ou via Yarn:

```bash
yarn global add @ualers/softwareai-skeleton-engine
```

### Scaffold de Projeto

```bash
# Gera esqueleto Flask no diretório `meu-projeto`
create-py-app meu-projeto --theme flask-web-product
```

Se não informar `--theme`, o padrão `flask-web-product` será utilizado.

### Agendamento de Agentes

```bash
# Agenda um agente para rodar em data/hora específica
create-py-app schedule-task \
  --agent "AgentsWorkFlow.Saas.teams.ProjectManager" \
  --email "usuario@exemplo.com" \
  --runAt "2025-05-20T15:30:00" \
  --repo "https://github.com/usuario/meu-projeto.git" \
  --params '{"session_id":"abc123","user_message":"Iniciar projeto"}'
```

Esse comando envia ao servidor:

```json
{
  "agent": "AgentsWorkFlow.Saas.teams.ProjectManager",
  "run_at": "2025-05-20T15:30:00-03:00",
  "repo_git": "https://github.com/usuario/meu-projeto.git",
  "params": {
    "user_email": "usuario@exemplo.com",
    "session_id": "abc123",
    "user_message": "Iniciar projeto"
  }
}
```

### Executando Localmente

1. Entre no diretório do projeto:

   ```bash
   cd meu-projeto
   ```
2. (Opcional) Crie e ative um virtualenv:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Instale dependências:

   ```bash
   pip install -r requirements.txt
   ```
4. Inicie a aplicação:

   ```bash
   python app.py
   ```

Ou com Docker Compose:

```bash
docker-compose up --build
```

Acesse em: `http://localhost:5000`

## Configuração da API de Agendamento

Defina a URL do servidor de agendamento (opcional, padrão: `http://localhost:5100`):

```bash
export SCHEDULER_API_URL=https://seu-servidor.com
```

## Contribuição

1. Faça um fork
2. Crie uma branch (`git checkout -b feature/x`)
3. Commit e push
4. Abra um Pull Request

## Licença

MIT
