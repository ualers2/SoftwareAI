# Back-End\Modules\Geters\logs.py

from Models.mongoDB.logs import logs_collection, mongo_db
from datetime import datetime, timedelta

def get_recent_logs(user_id=None, limit=10):
    """
    Retorna os logs mais recentes. Se user_id fornecido, filtra por user_id ou user.
    Cada log terá 'timestamp' como ISO string.
    """
    query = {}
    if user_id is not None:
        query = {"$or": [{"user_id": user_id}, {"user": user_id}]}

    raw = list(logs_collection.find(query).sort("timestamp", -1).limit(limit))
    adapted = []
    for log in raw:
        ts = log.get("timestamp")
        try:
            ts_iso = ts.isoformat() if hasattr(ts, "isoformat") else str(ts)
        except Exception:
            ts_iso = str(ts)
        adapted.append({
            "_id": str(log.get("_id")),
            "timestamp": ts_iso,
            "level": log.get("level"),
            "action": log.get("action"),
            "details": log.get("details", {}),
            "prNumber": log.get("prNumber") or (log.get("details") or {}).get("pr_number") or (log.get("details") or {}).get("prNumber"),
            "user": log.get("user"),
            "user_id": log.get("user_id")
        })
    return adapted

def get_logs_by_user(user, limit=50):
    """
    Recupera logs por usuário.
    """
    return list(
        logs_collection.find({"user": user})
        .sort("timestamp", -1)
        .limit(limit)
    )

def get_audit_trail(entity=None, limit=50):
    """
    Recupera auditorias do MongoDB.
    """
    audit_collection = mongo_db['audit_trail']
    query = {}
    if entity:
        query["entity"] = entity

    return list(
        audit_collection.find(query)
        .sort("timestamp", -1)
        .limit(limit)
    )

def get_system_health_recent(limit=50):
    """
    Recupera registros recentes de health_check.
    """
    system_health_collection = mongo_db['system_health']
    return list(
        system_health_collection.find({})
        .sort("timestamp", -1)
        .limit(limit)
    )

def get_system_health_by_user(user_id, limit=50):
    """
    Recupera registros de health_check filtrados por usuário.
    """
    system_health_collection = mongo_db['system_health']
    return list(
        system_health_collection.find({"user_id": user_id})
        .sort("timestamp", -1)
        .limit(limit)
    )

def get_system_health_by_status(status, limit=50):
    """
    Recupera registros de health_check filtrados por status (ok, warning, error).
    """
    system_health_collection = mongo_db['system_health']
    return list(
        system_health_collection.find({"status": status})
        .sort("timestamp", -1)
        .limit(limit)
    )