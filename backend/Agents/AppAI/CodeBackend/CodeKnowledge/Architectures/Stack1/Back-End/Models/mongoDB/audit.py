from datetime import datetime, timedelta
from pymongo import MongoClient
from dotenv import load_dotenv
import os

MONGO_URI = os.getenv('MONGO_URI', 'None')
MONGO_DB_NAME = os.getenv('MONGO_DB_NAME', 'controls_logs')
if MONGO_URI == 'None':
    load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../', '../',  'Keys', 'keys.env'))
    MONGO_URI = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')


mongo_client = MongoClient(MONGO_URI)
mongo_db = mongo_client[MONGO_DB_NAME]
logs_collection = mongo_db.logs

class AuditTrail:
    collection = mongo_db['audit_trail']

    @classmethod
    def create(cls, entity, action, user, metadata=None):
        entry = {
            "entity": entity,
            "action": action,
            "user": user,
            "metadata": metadata or {},
            "timestamp": datetime.utcnow()
        }
        result = cls.collection.insert_one(entry)
        return str(result.inserted_id)

    @classmethod
    def find_by_entity(cls, entity):
        return list(cls.collection.find({"entity": entity}).sort("timestamp", -1))