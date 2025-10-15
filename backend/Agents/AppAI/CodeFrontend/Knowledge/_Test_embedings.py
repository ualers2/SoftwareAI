# requirements: openai, openai-agents, chromadb, tiktoken (opcional)
# pip install openai openai-agents chromadb

import os
from agents import Agent, Runner, function_tool, SQLiteSession
import openai
import chromadb
from chromadb.config import Settings
from dotenv import load_dotenv
from openai import OpenAI


os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'keys.env'))

OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

# ---------- 2) Tool retriever: função registrada no SDK ----------
@function_tool
def retrieve_backend_context(query: str, k: int = 4) -> str:
    client_chroma = chromadb.PersistentClient(path="./chroma_store")
    collection = client_chroma.get_collection("backend_skeleton")

    q_emb = client.embeddings.create(
        model="text-embedding-3-small",
        input=[query]
    ).data[0].embedding

    results = collection.query(
        query_embeddings=[q_emb],
        n_results=k,
        include=["documents", "metadatas"]
    )

    docs = results["documents"][0]
    joined = "\n\n---\n\n".join(docs)
    return f"Contexto recuperado (top {k}):\n\n{joined}"

# # ---------- 3) Agente + sessão + runner ----------
# agent = Agent(
#     name="BackendExpert",
#     instructions="Você é um especialista backend. Use as ferramentas quando precisar recuperar regras/estrutura do projeto.",
#     tools=[retrieve_backend_context]
# )

# # usar SQLiteSession (memória persistente entre turns)
# session = SQLiteSession("agent_session_backend_01", db_path="embeddings.db")

# # entrada do usuário
# user_input = "Como eu crio o endpoint de login seguindo a stack padrão do projeto?"

# # rodar (Runner vai permitir tool calls automaticamente)
# result = Runner.run_sync(agent, user_input, session=session, max_turns=6)

# print("Resposta final do agente:\n", result.final_output)
