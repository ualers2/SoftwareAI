# Back-End\Models\postgreSQL.py
from flask_sqlalchemy import SQLAlchemy
import bcrypt
from datetime import datetime, timedelta
import secrets


TOKEN_DEFAULT_EXPIRES_DAYS = 30

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    plan_name = db.Column(db.String(128), default="Free", nullable=True)
    limit_monthly_tokens = db.Column(db.Integer, default=300000)
    tokens_used = db.Column(db.Integer, default=0)
    acess_token = db.Column(db.String(255), nullable=True)
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

class PullRequest(db.Model):
    __tablename__ = 'pull_requests'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    pr_number = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.Text, nullable=True)
    body = db.Column(db.Text, nullable=True)
    ai_generated_content = db.Column(db.Text, nullable=True) 
    original_diff = db.Column(db.Text, nullable=True)  
    total_tokens = db.Column(db.Integer, nullable=True) 
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, error
    diff_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    processed_by = db.Column(db.String(80))
    error_message = db.Column(db.String(255), nullable=True)

class Deployment(db.Model):
    __tablename__ = 'deployments'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    status = db.Column(db.String(50), default='pending')  # pending, in_progress, completed, failed
    triggered_by = db.Column(db.String(80), nullable=False)
    source = db.Column(db.String(50), default='manual')  # manual, webhook, scheduled
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    error_message = db.Column(db.Text)

class SystemHealth(db.Model):
    __tablename__ = 'system_health'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    postgres_status = db.Column(db.Boolean, default=True)
    mongodb_status = db.Column(db.Boolean, default=True)
    github_status = db.Column(db.Boolean, default=True)
    openai_status = db.Column(db.Boolean, default=True)
    last_check = db.Column(db.DateTime, default=datetime.utcnow)

class SystemSettings(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    github_token = db.Column(db.Text, nullable=True)
    github_secret = db.Column(db.Text, nullable=True)
    repository_name = db.Column(db.String(255), nullable=True)
    openai_api_key = db.Column(db.Text, nullable=True)
    webhook_url = db.Column(db.String(500), nullable=True)
    auto_process_prs = db.Column(db.Boolean, default=True)
    enable_logging = db.Column(db.Boolean, default=True)
    log_level = db.Column(db.String(50), default='INFO')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
