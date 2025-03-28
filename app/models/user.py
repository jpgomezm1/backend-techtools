from datetime import datetime
import re
from app.extensions import mongo

class User:
    """
    Clase para manejar las operaciones con usuarios en MongoDB
    """
    
    @staticmethod
    def validate_email(email):
        """Validar formato de email"""
        email_pattern = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
        return bool(re.match(email_pattern, email))
    
    @staticmethod
    def create_user(user_data):
        """
        Crear un nuevo usuario en la base de datos
        
        Args:
            user_data (dict): Datos del usuario a crear
            
        Returns:
            tuple: (bool, dict or str) - (éxito, datos del usuario o mensaje de error)
        """
        # Validar campos requeridos
        required_fields = ['name', 'email', 'country', 'userType']
        for field in required_fields:
            if field not in user_data or not user_data[field]:
                return False, f"El campo {field} es requerido"
        
        # Validar email
        if not User.validate_email(user_data['email']):
            return False, "El formato del email no es válido"
        
        # Validar campos específicos según tipo de usuario
        if user_data['userType'] == 'Empresa':
            if 'company' not in user_data or not user_data['company']:
                return False, "El campo company es requerido para empresas"
            if 'automationNeeds' not in user_data or not user_data['automationNeeds']:
                return False, "El campo automationNeeds es requerido para empresas"
        
        elif user_data['userType'] in ['Emprendedor', 'Freelancer', 'Persona']:
            if 'interestArea' not in user_data or not user_data['interestArea']:
                return False, "El campo interestArea es requerido"
            if 'toolsUsed' not in user_data or not user_data['toolsUsed']:
                return False, "El campo toolsUsed es requerido"
            if 'projectDescription' not in user_data or not user_data['projectDescription']:
                return False, "El campo projectDescription es requerido"
        
        # Verificar si el email ya existe
        existing_user = mongo.db.users.find_one({'email': user_data['email']})
        if existing_user:
            return False, "Este email ya está registrado"
        
        # Añadir fecha de registro
        user_data['registrationDate'] = datetime.utcnow()
        user_data['isVerified'] = False
        
        # Insertar en la base de datos
        result = mongo.db.users.insert_one(user_data)
        
        if result.inserted_id:
            # Recuperar el usuario insertado
            new_user = mongo.db.users.find_one({'_id': result.inserted_id})
            # Convertir ObjectId a string para poder serializarlo a JSON
            new_user['_id'] = str(new_user['_id'])
            return True, new_user
        
        return False, "Error al crear el usuario"
    
    @staticmethod
    def find_by_email(email):
        """Buscar usuario por email"""
        user = mongo.db.users.find_one({'email': email})
        if user:
            user['_id'] = str(user['_id'])
        return user