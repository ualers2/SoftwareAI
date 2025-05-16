from firebase_admin import auth, credentials, db
import time

def store_github_session_in_firebase(username, github_id, access_token, appcompany):
    ref = db.reference(f"sessions/github/{username}", app=appcompany)
    
    # Timestamp atual + 30 dias
    expiration_ts = int(time.time()) + 30 * 24 * 60 * 60

    ref.set({
        "username": username,
        "github_id": github_id,
        "access_token": access_token,
        "expires_at": expiration_ts
    })
