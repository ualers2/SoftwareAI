# app.py
import os
import threading
import requests
import json
import stripe
import asyncio
from decimal import Decimal
from bson.json_util import dumps
from datetime import datetime, timedelta, timezone
import hmac
import hashlib
from flask import g, Flask, Response, request, jsonify, send_file, abort, redirect
from flask_cors import CORS
from asgiref.wsgi import WsgiToAsgi
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


from Models.postgreSQL.user import db
from Modules.Config.setup import Settings
from Modules.Routes.auth import auth_bp

app = Flask(__name__)
asgi_app = WsgiToAsgi(app)
settings = Settings()

app.config['SQLALCHEMY_DATABASE_URI'] = settings.SQLALCHEMY_DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET'] = settings.JWT_SECRET
app.config['MONGO_URI'] = settings.MONGO_URI
app.config['SECRET_KEY'] = settings.SECRET_KEY

INVOICES_DIR = settings.INVOICES_DIR
SMTP_HOST = settings.SMTP_HOST
SMTP_PORT = settings.SMTP_PORT
SMTP_USER = settings.SMTP_USER
SMTP_PASSWORD = settings.SMTP_PASSWORD
use_tls = settings.use_tls
stripe.api_key  = settings.STRIPE_SECRET_KEY

if os.getenv("FLASK_ENV") == "development":
    CORS(app, origins=os.getenv("FRONTEND_ORIGINS", "*").split(","), supports_credentials=True)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=[]
)

db.init_app(app)

@app.route('/')
def index():
    return jsonify({
        "message": "Backend Flask - API Principal",
        "version": "1.0",
        "database": "PostgreSQL + MongoDB",
        "status": "running"
    })


app.register_blueprint(auth_bp, url_prefix='/auth')

