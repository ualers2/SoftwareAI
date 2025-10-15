
from Models.postgreSQL import db, User
from datetime import datetime, timedelta

def get_user_by_access_token(token_str):
    if not token_str:
        return None
    return User.query.filter_by(acess_token=token_str).first()
