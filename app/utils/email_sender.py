# app/utils/email_sender.py
import os
import requests
from flask import current_app

def send_welcome_email(user_data):
    """
    Envía un correo de bienvenida al usuario recién registrado.
    
    Args:
        user_data (dict): Datos del usuario registrado (nombre, email, etc.)
    
    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario
    """
    try:
        # Obtener configuración de Mailgun
        api_key = current_app.config.get('MAILGUN_API_KEY')
        domain = current_app.config.get('MAILGUN_DOMAIN')
        sender_email = current_app.config.get('SENDER_EMAIL')
        
        if not all([api_key, domain, sender_email]):
            current_app.logger.error("Faltan configuraciones de Mailgun")
            return False
        
        # URL de la API de Mailgun
        url = f"https://api.mailgun.net/v3/{domain}/messages"
        
        # Datos del correo
        data = {
            "from": f"Irrelevant Club <{sender_email}>",
            "to": user_data['email'],
            "subject": "¡Bienvenido al arsenal de herramientas tech de Irrelevant!",
            "text": f"""
            ¡Hola {user_data['name']}!
            
            Gracias por unirte a nuestro arsenal de herramientas tech. Estamos emocionados de tenerte como parte de la comunidad.
            
            Accede a todas las herramientas, guías y recursos que hemos preparado para ti. Recuerda que puedes ingresar con la frase secreta: "soy irrelevant club".
            
            Si tienes alguna pregunta, no dudes en contactarnos.
            
            ¡A construir proyectos increíbles!
            Equipo Irrelevant
            """,
            "html": f"""
            <html>
                <head>
                    <style>
                        body {{ font-family: Arial, sans-serif; color: #333; line-height: 1.6; }}
                        .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                        .header {{ background: linear-gradient(to right, #9C6BFF, #A566FF); color: white; padding: 20px; border-radius: 10px 10px 0 0; }}
                        .content {{ background-color: #f9f9f9; padding: 20px; border-radius: 0 0 10px 10px; }}
                        .button {{ display: inline-block; background: linear-gradient(to right, #9C6BFF, #A566FF); color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; margin: 20px 0; }}
                        .footer {{ margin-top: 20px; font-size: 12px; color: #888; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <div class="header">
                            <h1>¡Bienvenido a Irrelevant Club!</h1>
                        </div>
                        <div class="content">
                            <p>¡Hola <strong>{user_data['name']}</strong>!</p>
                            
                            <p>Gracias por unirte a nuestro arsenal de herramientas tech. Estamos emocionados de tenerte como parte de la comunidad.</p>
                            
                            <p>Accede a todas las herramientas, guías y recursos que hemos preparado para ti. Recuerda que puedes ingresar con la frase secreta: <strong>"soy irrelevant club"</strong>.</p>
                            
                            <a href="https://stayirrelevant.com" class="button">Explorar Herramientas</a>
                            
                            <p>Si tienes alguna pregunta, no dudes en contactarnos.</p>
                            
                            <p>¡A construir proyectos increíbles!<br>
                            <strong>Equipo Irrelevant</strong></p>
                        </div>
                        <div class="footer">
                            <p>© {user_data.get('registrationDate', '2025')} Irrelevant Club. Todos los derechos reservados.</p>
                        </div>
                    </div>
                </body>
            </html>
            """
        }
        
        # Enviar correo usando la API de Mailgun
        response = requests.post(
            url,
            auth=("api", api_key),
            data=data
        )
        
        # Verificar respuesta
        if response.status_code == 200:
            current_app.logger.info(f"Correo enviado exitosamente a {user_data['email']}")
            return True
        else:
            current_app.logger.error(f"Error al enviar correo: {response.text}")
            return False
            
    except Exception as e:
        current_app.logger.error(f"Error en el envío de correo: {str(e)}")
        return False