# Back-End\Models\postgreSQL.py
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
    
class CommitMessage(db.Model):
    __tablename__ = 'commit_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    title = db.Column(db.String(255), nullable=True)
    author = db.Column(db.String(255), nullable=True)
    commit_hash = db.Column(db.String(40), unique=True, nullable=False)  # hash do commit
    message = db.Column(db.Text, nullable=True)  # mensagem do commit
    ai_generated_message = db.Column(db.Text, nullable=True)  # caso a mensagem seja gerada por IA
    original_diff = db.Column(db.Text, nullable=True) 
    total_tokens = db.Column(db.Integer, nullable=True)  # tokens usados pela IA
    status = db.Column(db.String(50), default='pending')  # pending, processing, completed, error
    pr_linked_id = db.Column(db.Integer, db.ForeignKey('pull_requests.id'), nullable=True)  # link para PR, se houver
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    processed_at = db.Column(db.DateTime, nullable=True)
    processed_by = db.Column(db.String(80))
    error_message = db.Column(db.String(255), nullable=True)
    
    pull_request = db.relationship("PullRequest", backref=db.backref("commit_messages", lazy=True))

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
    installation_id = db.Column(db.BigInteger, nullable=True)  
    github_token = db.Column(db.Text, nullable=True)
    github_secret = db.Column(db.Text, nullable=True)
    repository_name = db.Column(db.String(255), nullable=True)

    throttle_ms = db.Column(db.Integer, nullable=True)
    lines_threshold = db.Column(db.Integer, nullable=True)
    files_threshold = db.Column(db.Integer, nullable=True)
    time_threshold = db.Column(db.Integer, nullable=True)
    auto_push = db.Column(db.Boolean, default=False)
    auto_create_pr = db.Column(db.Boolean, default=False)
    commit_language = db.Column(db.String(255), nullable=True)

    auto_process_prs = db.Column(db.Boolean, default=True)


    openai_api_key = db.Column(db.Text, nullable=True)
    webhook_url = db.Column(db.String(500), nullable=True)
    enable_logging = db.Column(db.Boolean, default=True)
    log_level = db.Column(db.String(50), default='INFO')
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class Invoice(db.Model):
    __tablename__ = 'invoices'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    number = db.Column(db.String(64), nullable=False)  # número/identificador da fatura
    date = db.Column(db.DateTime, default=datetime.utcnow)
    amount = db.Column(Numeric(12, 2), nullable=False, default=0.0)
    currency = db.Column(db.String(8), default='BRL')
    status = db.Column(db.String(32), default='pending')  # paid, pending, failed
    plan_name = db.Column(db.String(128), nullable=True)
    pdf_path = db.Column(db.String(500), nullable=True)  # path relativo em ./invoices/ ou None
    pdf_url = db.Column(db.String(1000), nullable=True)  # opcional: url externa se armazenada em S3 etc.
    lines = db.Column(db.Text, nullable=True)  # JSON serializado com itens [{description, qty, price}, ...]
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self, include_lines=False):
        data = {
            "id": str(self.id),
            "number": self.number,
            "date": self.date.isoformat() if self.date else None,
            "amount": float(self.amount) if self.amount is not None else 0.0,
            "currency": self.currency,
            "status": self.status,
            "planName": self.plan_name,
            "pdfUrl": self.pdf_url or (f"/api/invoices/{self.id}/download" if self.pdf_path else None)
        }
        if include_lines:
            try:
                data["lines"] = json.loads(self.lines) if self.lines else []
            except Exception:
                data["lines"] = []
        return data
