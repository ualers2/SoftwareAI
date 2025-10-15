import requests
from datetime import datetime, timedelta
import pytz
from pydantic import BaseModel
import os
from agents import Agent, Runner, function_tool, SQLiteSession
import openai
import chromadb
from openai import OpenAI
from dotenv import load_dotenv

@function_tool
def task_sheduler(
                BACKEND_URL: str,
                ACCESS_TOKEN: str,
                EMPLOYER_CATEGORY: str,
                SPRINT_NAME: str,
                SPRINT_OBJECTIVE: str,
                user_id: int = 4, 
                priority: int = 2, 
                hours: str = '1.5',
                lang: str ='pt',
                eta_str: str | None = None
                ) -> str:
    tz = pytz.timezone("America/Sao_Paulo")
    if eta_str:
        try:
            eta = datetime.strptime(eta_str, "%Y-%m-%d %H:%M:%S")
            eta = tz.localize(eta)
        except ValueError:
            raise ValueError("Formato de data inválido! Use 'YYYY-MM-DD HH:MM:SS'")
    else:
        eta = datetime.now(tz) + timedelta(minutes=2)

    print(f"⏰ Tarefa agendada para {eta.strftime('%Y-%m-%d %H:%M:%S')} (Horário de São Paulo)")

    payload = {
        "user_id": user_id,
        "category": EMPLOYER_CATEGORY,
        "content": f"Tarefa para {SPRINT_NAME}\n\n{SPRINT_OBJECTIVE}",
        "priority": priority,
        "hours": hours,
        "lang": lang,
        "eta": eta.isoformat()  # Passando ISO 8601
    }

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
            return f"🆔 ID da tarefa: {data.get('task_id')}"
        else:
            print(f"❌ Falha ao criar tarefa ({response.status_code}): {response.text}")
            return f"❌ Falha ao criar tarefa ({response.status_code}): {response.text}"
    except Exception as e:
        print(f"💥 Erro de execução: {e}")
