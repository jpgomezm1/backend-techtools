from flask import Blueprint, request, jsonify, current_app
from app.models.user import User
from app.utils.auth import generate_token
from app.utils.email_sender import send_welcome_email

user_bp = Blueprint('users', __name__)

@user_bp.route('/register', methods=['POST'])
def register():
    """
    Endpoint para registrar un nuevo usuario
    """
    data = request.json
    
    if not data:
        return jsonify({'message': 'No se proporcionaron datos'}), 400
    
    success, result = User.create_user(data)
    
    if success:
        # Generar token para el usuario
        token = generate_token(str(result['_id']))
        
        # Preparar respuesta con datos básicos y token
        response = {
            '_id': result['_id'],
            'name': result['name'],
            'email': result['email'],
            'userType': result['userType'],
            'country': result['country'],
            'token': token
        }
        
        # Enviar correo de bienvenida (asíncrono para no bloquear la respuesta)
        try:
            # Para el sandbox, necesitas añadir destinatarios autorizados
            # Solo enviamos correo si el usuario está en tu lista de destinatarios autorizados
            send_welcome_email(result)
            current_app.logger.info(f"Correo de bienvenida enviado a {result['email']}")
        except Exception as e:
            # Registro del error pero continuamos con el flujo
            current_app.logger.error(f"Error al enviar correo: {str(e)}")
        
        return jsonify(response), 201
    else:
        return jsonify({'message': result}), 400

@user_bp.route('/verify-phrase', methods=['POST'])
def verify_secret_phrase():
    """
    Endpoint para verificar la frase secreta
    """
    data = request.json
    
    if not data or 'secretPhrase' not in data:
        return jsonify({'message': 'Frase secreta no proporcionada'}), 400
    
    # Comparar con la frase secreta almacenada en la configuración
    if data['secretPhrase'].lower().strip() == current_app.config['SECRET_PHRASE'].lower():
        # Generar token especial
        token = generate_token('special-access')
        
        return jsonify({
            'success': True,
            'message': 'Frase secreta correcta',
            'token': token
        }), 200
    else:
        return jsonify({
            'success': False,
            'message': 'Frase secreta incorrecta'
        }), 401