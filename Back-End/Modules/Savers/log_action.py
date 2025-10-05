# Back-End\Modules\Savers\log_action.py
from datetime import datetime, timedelta
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


def log_action(logs_collection, action, details=None, user=None, level='info'):
    """
    Registra uma ação no MongoDB (coleção logs).
    Padroniza campos: timestamp (UTC), level uppercase, user_id (se for int), user (se for string/obj), details como dict.
    """
    if details is None:
        details = {}

    if not isinstance(details, dict):
        try:
            details = {"message": str(details)}
        except Exception:
            details = {"message": "no details"}

    if "message" not in details:
        details["message"] = details.get("msg") or str(action)

    user_id_val = None
    user_val = None
    if user is not None:
        try:
            user_id_val = int(getattr(user, "id", user))
        except Exception:
            user_val = str(user)
    if isinstance(user, int):
        user_id_val = user
        user_val = user

    log_entry = {
        "timestamp": datetime.utcnow(),  
        "action": action,
        "details": details,
        "level": (level or "info").upper()
    }

    if user_id_val is not None:
        log_entry["user_id"] = user_id_val
        log_entry["user"] = user_id_val
    elif user_val is not None:
        log_entry["user"] = user_val

    if "prNumber" in details and "pr_number" not in details:
        details["pr_number"] = details["prNumber"]

    logger.info(f"""
timestamp {datetime.utcnow().isoformat()}
action {action}
details {details}
user {user}
level {level}
    """)
    result = logs_collection.insert_one(log_entry)
    return str(result.inserted_id)