# app/config.py
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-change-in-production')
    MONGO_URI = os.environ.get('MONGO_URI', 'mongodb://localhost:27017/irrelevant-toolkit')
    SECRET_PHRASE = os.environ.get('SECRET_PHRASE', 'soy irrelevant club')
    JWT_EXPIRATION_DAYS = 30
    
    # Configuración de Mailgun
    MAILGUN_API_KEY = os.environ.get('MAILGUN_API_KEY')
    MAILGUN_DOMAIN = os.environ.get('MAILGUN_DOMAIN', 'sandbox8b842af5fbad4b598617e8be8a7e0e8b.mailgun.org')
    SENDER_EMAIL = os.environ.get('SENDER_EMAIL', 'mailgun@sandbox8b842af5fbad4b598617e8be8a7e0e8b.mailgun.org')