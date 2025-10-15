import requests
from datetime import datetime, timedelta
import pytz

# URL base do seu backend Flask
BACKEND_URL = "http://localhost:5910/api/tasks/add"  # ajuste se estiver em outra porta/host
ACCESS_TOKEN = "IJGpuZxIP0eIJRfpzUsuCMbOEkq0dwR-Lq8sY2Uo-o0"  # substitua pelo token JWT real do usuário autenticado

# 🧠 Conteúdo da Sprint 3
SPRINT_NAME = "## Sprint 1 | Intervalo de horas: 1-4"
SPRINT_OBJECTIVE = """

Descrição do produto: sistema multiusuário (médicos e pacientes) para agendamento online de consultas com pagamento integrado via Stripe. Backend em Flask, PostgreSQL, Redis; Front-end em Vite + React; Observabilidade com MongoDB; Orquestração de tarefas com Celery + Redis; CI/CD com GitHub Actions.

### MVP Base
- Configurar estrutura do projeto Flask API + PostgreSQL + Redis
- Criar containers Docker
- Definir arquitetura de pastas
- desenvolvimento dos endpoints

## Sprint 1 | Intervalo de horas: 1-4
* [x] Configuração inicial do projeto (Flask + PostgreSQL + MongoDB)
* [x] Setup de ambiente e containers Docker
* [x] Implementar `/api/register` e `/api/login`
* [x] Configuração de AUth 
* [x] Persistência de usuários no PostgreSQL
* [x] Integração com MongoDB para logs
* [x] Implementar endpoints `/api/logs` e `/api/logs/export`
* [x] Função `log_action` com salvamento estruturado de ações
* [x] Implementar `/api/settings` (GET/PUT)
* [x] Endpoint `/api/health` para checagem completa de serviços
* [x] Modelagem de médicos e pacientes no Postgres
* [x] Endpoint `/api/médicos` (listagem)
* [x] Endpoint `/api/médicos/<id>` (detalhes)
* [x] Endpoint `/api/pacientes` (listagem)
* [x] Endpoint `/api/pacientes/<id>` (detalhes)
* [x] Endpoint `/api/dashboard-data` com estatísticas e atividades do sistema

"""

tz = pytz.timezone("America/Sao_Paulo")

now_sp = datetime.now(tz)

eta = now_sp + timedelta(minutes=2)
print(f"⏰ Tarefa agendada para {eta} ")

# Corpo da requisição
payload = {
    "user_id": 1,
    "content": f"Tarefa para {SPRINT_NAME}\n\n{SPRINT_OBJECTIVE}",
    "priority": 2,
    "hours": "1.5",
    "lang": "pt",
    "eta": eta.isoformat()  # Passando ISO 8601
}

# Cabeçalhos (autenticação + JSON)
headers = {
    "Content-Type": "application/json",
    "X-API-TOKEN": ACCESS_TOKEN
}

try:
    response = requests.post(BACKEND_URL, json=payload, headers=headers)
    if response.status_code == 201:
        data = response.json()
        print("✅ Tarefa criada com sucesso!")
        print(f"🆔 ID da tarefa: {data.get('task_id')}")
        print(f"📦 Status inicial: {data.get('status')}")
    else:
        print(f"❌ Falha ao criar tarefa ({response.status_code}): {response.text}")
except Exception as e:
    print(f"💥 Erro de execução: {e}")
