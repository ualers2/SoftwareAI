from pydantic import BaseModel
import os
from agents import Agent, Runner, function_tool, SQLiteSession
import openai
import chromadb
from openai import OpenAI
from dotenv import load_dotenv
# load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), "../", "../", "../", 'Keys', 'keys.env'))

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
client = OpenAI(api_key=OPENAI_API_KEY)

@function_tool
def retrieve_backend_context(query: str, k: int = 4, path: str = "./CodeKnowledge/chroma_store", name: str ='backend_skeleton') -> str:
    client_chroma = chromadb.PersistentClient(path=path)
    collection = client_chroma.get_collection(name)

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

# if __name__ == '__main__':
#     content = retrieve_backend_context("Flask blueprint authentication patterns: user model, registration, login, password hashing, JWT tokens, SQLAlchemy integration", 8, path=os.path.join(os.path.dirname(__file__), 'CodeKnowledge', 'chroma_store'))
#     print(content)