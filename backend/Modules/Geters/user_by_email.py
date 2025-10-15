
from Models.postgreSQL import db, User
from datetime import datetime, timedelta

def get_user_by_email(email):
    if not email:
        return None
    return User.query.filter_by(email=email).first()
