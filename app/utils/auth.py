import jwt
import datetime
from flask import current_app, request, jsonify
from functools import wraps

def generate_token(user_id):
    """
    Generar un token JWT para el usuario
    
    Args:
        user_id (str): ID del usuario o 'special-access' para acceso especial
        
    Returns:
        str: Token JWT generado
    """
    # Obtener configuración
    secret_key = current_app.config['SECRET_KEY']
    expiration_days = current_app.config.get('JWT_EXPIRATION_DAYS', 30)
    
    # Crear payload
    payload = {
        'user_id': user_id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=expiration_days),
        'iat': datetime.datetime.utcnow()
    }
    
    # Generar token
    token = jwt.encode(payload, secret_key, algorithm='HS256')
    
    return token

def token_required(f):
    """
    Decorador para proteger rutas que requieren autenticación
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Extraer token del header
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.split(' ')[1]
            
        if not token:
            return jsonify({'message': 'Token no proporcionado'}), 401
        
        try:
            # Decodificar token
            secret_key = current_app.config['SECRET_KEY']
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            
            # Añadir información del usuario al contexto de la petición
            request.user_id = payload['user_id']
            request.is_special_access = payload['user_id'] == 'special-access'
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token expirado. Por favor, inicia sesión nuevamente.'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Token inválido. Por favor, inicia sesión nuevamente.'}), 401
        
        return f(*args, **kwargs)
    
    return decorated