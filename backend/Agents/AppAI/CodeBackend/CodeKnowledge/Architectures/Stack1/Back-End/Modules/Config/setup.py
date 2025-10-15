import logging
import os
from dotenv import load_dotenv

class Settings:
    def __init__(self):
        self.ENV = __import__('os').environ.get('FLASK_ENV', 'development')
        self.SQLALCHEMY_DATABASE_URI = __import__('os').environ.get('DATABASE_URL', 'postgresql://postgres:postgres@meu_postgres2:5432/meubanco')
        self.MONGO_URI = __import__('os').environ.get('MONGO_URI', 'mongodb://root:rootpassword@mongodb:27017/controls_logs?authSource=admin')
        self.CELERY_BROKER_URL = __import__('os').environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
        self.CELERY_RESULT_BACKEND = __import__('os').environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
        self.JWT_SECRET = __import__('os').environ.get('JWT_SECRET', 'supersecret')
        self.SECRET_KEY = __import__('os').environ.get('SECRET_KEY', 'your-secret-key-here')

        diretorio_script = os.path.dirname(os.path.abspath(__file__)) 
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        os.makedirs(os.path.join(diretorio_script, '../', '../', 'Logs'), exist_ok=True)
        file_handler = logging.FileHandler(os.path.join(diretorio_script, '../', '../', 'Logs', 'api.log'))
        file_handler.setFormatter(formatter)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        self.logger = logger

        load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../', '../', "Keys", 'keys.env'))


        self.INVOICES_DIR = os.path.join(os.path.dirname(__file__), '../', '../', 'Invoices')
        os.makedirs(self.INVOICES_DIR, exist_ok=True)


        self.SMTP_HOST = os.getenv('SMTP_HOST')
        self.SMTP_PORT = int(os.getenv('SMTP_PORT', 587))
        self.SMTP_USER = os.getenv('SMTP_USER')
        self.SMTP_PASSWORD = os.getenv('SMTP_PASSWORD')
        self.use_tls = os.getenv('SMTP_USE_TLS', 'true').lower() == 'true'

        self.STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY")
        