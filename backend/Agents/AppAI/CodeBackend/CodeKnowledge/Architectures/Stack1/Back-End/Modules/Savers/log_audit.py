# Back-End\Modules\Savers\log_audit.py

from datetime import datetime, timedelta
from Models.mongoDB.audit import mongo_db

audit_collection = mongo_db['audit_trail']

def log_audit(entity, action, user=None, metadata=None):
    """
    Registra uma auditoria no MongoDB (coleção audit_trail).
    """
    entry = {
        "entity": entity,
        "action": action,
        "user": user,
        "metadata": metadata or {},
        "timestamp": datetime.utcnow()
    }
    result = audit_collection.insert_one(entry)
    return str(result.inserted_id)

