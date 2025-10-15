# Back-End\Modules\Savers\log_system_health.py
from datetime import datetime, timedelta
from Models.mongoDB import mongo_db

system_health_collection = mongo_db['system_health']

def log_system_health(user_id, health_status: dict):
    """
    Registra status de saúde do sistema no MongoDB (coleção system_health).
    """
    entry = {
        "user_id": user_id,
        "timestamp": datetime.utcnow(),
        "postgres_status": health_status.get("postgres_connected", False),
        "mongodb_status": health_status.get("mongodb_connected", False),
        "github_status": health_status.get("github_api_reachable", False),
        "openai_status": health_status.get("openai_api_reachable", False),
        "status": health_status.get("status", "unknown"),
        "message": health_status.get("message", ""),
        "details": health_status
    }
    result = system_health_collection.insert_one(entry)
    return str(result.inserted_id)
