# user.py
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime, timedelta
import secrets
import json
from sqlalchemy import Numeric

TOKEN_DEFAULT_EXPIRES_DAYS = 30

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    acess_token = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    revoked_at = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))
        
    def create_access_token_for_user(self, expires_days: int = TOKEN_DEFAULT_EXPIRES_DAYS):
        token = secrets.token_urlsafe(32)
        self.acess_token = token
        if expires_days:
            self.expires_at = datetime.utcnow() + timedelta(days=int(expires_days))
        self.revoked_at = None
        return token
    