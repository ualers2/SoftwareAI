
from datetime import datetime, timedelta
def get_tokens(numeric_user_id, log_action, logs_collection, SystemSettings, db):
    settings = SystemSettings.query.filter_by(user_id=numeric_user_id).first()
    if not settings:
        settings = SystemSettings(user_id=numeric_user_id)
        db.session.add(settings)
        try:
            db.session.commit()
        except Exception as e:
            log_action(logs_collection, 'reprocess_pr_error', {
                'note': f"Erro ao criar SystemSettings: {e}",
            }, user=numeric_user_id)
            
            db.session.rollback()

    GITHUB_TOKEN = settings.github_token
    OPENAI_API_KEY = settings.openai_api_key    
    GITHUB_SECRET = settings.github_secret
    REPOSITORY_NAME = settings.repository_name
    return GITHUB_TOKEN, OPENAI_API_KEY, GITHUB_SECRET, REPOSITORY_NAME

