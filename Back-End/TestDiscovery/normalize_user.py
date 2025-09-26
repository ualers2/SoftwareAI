# mock_log.py
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'Keys', 'keys.env'))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "controls_logs")

# Conexão com o Mongo
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
logs = db.logs

# normaliza user -> user_id onde possível
for doc in logs.find({"user_id": {"$exists": False}, "user": {"$exists": True}}):
    try:
        uid = int(doc.get("user"))
        logs.update_one({"_id": doc["_id"]}, {"$set": {"user_id": uid}})
    except Exception:
        pass
# normaliza detalhes de PR
for doc in logs.find({"details.prNumber": {"$exists": True}}):
    val = doc["details"]["prNumber"]
    logs.update_one({"_id": doc["_id"]}, {"$set": {"details.pr_number": val, "prNumber": val}})
