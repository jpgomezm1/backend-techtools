import os
from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import mongo
from app.routes.user_routes import user_bp

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    mongo.init_app(app)
    
    # Habilitar CORS
    CORS(app)
    
    # Registrar blueprints
    app.register_blueprint(user_bp, url_prefix='/api/users')
    
    # Ruta de prueba
    @app.route('/')
    def home():
        return {
            'message': 'Bienvenido a la API de irrelevant toolkit',
            'status': 'online'
        }
    
    return app