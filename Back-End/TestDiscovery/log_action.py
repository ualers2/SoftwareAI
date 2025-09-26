# mock_log.py
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv

os.chdir(os.path.join(os.path.dirname(__file__)))
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../',  'Keys', 'keys.env'))

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "controls_logs")

# Conexão com o Mongo
client = MongoClient(MONGO_URI)
db = client[MONGO_DB_NAME]
logs_collection = db.logs

# Inserir log mock
log_entry = {
    "timestamp": datetime.utcnow(),
    "level": "SUCCESS",
    "details": {
        'message': "Log de teste gerado manualmente",
        'processed_by': 'AI',
        'status': 'completed',
        'model': 'gpt-5-nano',

    },
    "action": "mock_script",
    "user_id": 1,
    "prNumber": 42
}

result = logs_collection.insert_one(log_entry)
print(f"✅ Log mock inserido com _id: {result.inserted_id}")
