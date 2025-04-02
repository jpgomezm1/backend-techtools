import os
import resend
from flask import current_app
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Configura la API key de Resend desde .env
resend.api_key = os.getenv("RESEND_API_KEY")

def send_welcome_email(user_data):
    """
    Envía un correo de bienvenida al usuario recién registrado usando Resend.

    Args:
        user_data (dict): Datos del usuario registrado (nombre, email, etc.)

    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario
    """
    try:
        # Obtener año actual para el footer
        current_year = datetime.utcnow().year

        # Preparar HTML y texto plano
        html_content = get_welcome_email_html(user_data, current_year)
        text_content = get_welcome_email_text(user_data, current_year)

        # Enviar correo usando Resend
        response = resend.Emails.send({
            "from": "irrelevant club <info@updates.stayirrelevant.com>",
            "to": [user_data['email']],
            "subject": "Welcome to irrelevant club",
            "html": html_content,
            "text": text_content
        })

        current_app.logger.info(f"Correo enviado exitosamente a {user_data['email']}")
        return True

    except Exception as e:
        current_app.logger.error(f"Error en el envío de correo: {str(e)}")
        return False

def notify_admin_new_registration(user_data):
    """
    Envía una notificación por correo a los administradores cuando hay un nuevo registro.

    Args:
        user_data (dict): Datos del usuario registrado (nombre, email, etc.)

    Returns:
        bool: True si el correo se envió correctamente, False en caso contrario
    """
    try:
        # Lista de administradores a notificar
        admin_emails = ["jpgomez@stayirrelevant.com", "ahoyosh@stayirrelevant.com"]
        
        # Crear el contenido del correo de notificación
        html_content = get_admin_notification_html(user_data)
        text_content = get_admin_notification_text(user_data)
        
        # Enviar correo usando Resend
        response = resend.Emails.send({
            "from": "irrelevant club <info@updates.stayirrelevant.com>",
            "to": admin_emails,
            "subject": f"Nuevo registro en irrelevant club: {user_data['name']}",
            "html": html_content,
            "text": text_content
        })
        
        current_app.logger.info(f"Notificación de nuevo registro enviada a los administradores")
        return True
        
    except Exception as e:
        current_app.logger.error(f"Error en el envío de notificación a administradores: {str(e)}")
        return False

def get_admin_notification_html(user_data):
    """
    Genera el HTML para la notificación de nuevo registro para administradores.

    Args:
        user_data (dict): Datos del usuario registrado

    Returns:
        str: HTML del correo de notificación
    """
    # Obtener fecha y hora actual
    now = datetime.utcnow()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S UTC")
    
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nuevo Registro en irrelevant club</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #14121f;
            border-radius: 16px;
            overflow: hidden;
            color: #e1e1e6;
        }}
        .header {{
            background: linear-gradient(125deg, #9C6BFF, #7A4FD3);
            padding: 20px;
            text-align: center;
        }}
        .header h1 {{
            margin: 0;
            font-size: 24px;
            color: white;
            letter-spacing: -0.5px;
            font-weight: 700;
        }}
        .content {{
            padding: 25px;
        }}
        .user-card {{
            background-color: #292841;
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 25px;
        }}
        .user-detail {{
            margin-bottom: 12px;
            display: flex;
        }}
        .detail-label {{
            font-weight: 600;
            min-width: 120px;
            color: #9C6BFF;
        }}
        .detail-value {{
            flex: 1;
            color: white;
        }}
        .timestamp {{
            background-color: rgba(156, 107, 255, 0.1);
            border-radius: 8px;
            padding: 10px 15px;
            margin-top: 20px;
            font-size: 14px;
            color: #9C6BFF;
            text-align: center;
        }}
        .footer {{
            background-color: #12101a;
            padding: 15px;
            text-align: center;
            font-size: 13px;
            color: #8e8e96;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎉 Nuevo Registro en irrelevant club</h1>
        </div>
        <div class="content">
            <p>Un nuevo usuario se ha registrado en la plataforma:</p>
            
            <div class="user-card">
                <div class="user-detail">
                    <div class="detail-label">Nombre:</div>
                    <div class="detail-value">{user_data['name']}</div>
                </div>
                <div class="user-detail">
                    <div class="detail-label">Email:</div>
                    <div class="detail-value">{user_data['email']}</div>
                </div>
                <div class="user-detail">
                    <div class="detail-label">Tipo de usuario:</div>
                    <div class="detail-value">{user_data.get('userType', 'No especificado')}</div>
                </div>
                <div class="user-detail">
                    <div class="detail-label">País:</div>
                    <div class="detail-value">{user_data.get('country', 'No especificado')}</div>
                </div>
            </div>
            
            <p>Ya se le ha enviado el correo de bienvenida automáticamente.</p>
            
            <div class="timestamp">
                Registro realizado el {timestamp}
            </div>
        </div>
        <div class="footer">
            <p>© {now.year} irrelevant. Sistema automático de notificaciones.</p>
        </div>
    </div>
</body>
</html>"""

def get_admin_notification_text(user_data):
    """
    Genera la versión de texto plano de la notificación de nuevo registro para administradores.

    Args:
        user_data (dict): Datos del usuario registrado

    Returns:
        str: Texto plano del correo de notificación
    """
    # Obtener fecha y hora actual
    now = datetime.utcnow()
    timestamp = now.strftime("%d/%m/%Y %H:%M:%S UTC")
    
    return f"""NUEVO REGISTRO EN IRRELEVANT CLUB

Un nuevo usuario se ha registrado en la plataforma:

DATOS DEL USUARIO:
Nombre: {user_data['name']}
Email: {user_data['email']}
Tipo de usuario: {user_data.get('userType', 'No especificado')}
País: {user_data.get('country', 'No especificado')}

Ya se le ha enviado el correo de bienvenida automáticamente.

Registro realizado el {timestamp}

© {now.year} irrelevant. Sistema automático de notificaciones.
"""

def get_welcome_email_text(user_data, current_year):
    """
    Genera la versión de texto plano del correo de bienvenida.

    Args:
        user_data (dict): Datos del usuario
        current_year (int): Año actual para el footer

    Returns:
        str: Texto plano del correo
    """
    return f"""
Acabas de entrar al lado oscuro de la automatización.

Hola {user_data['name']},

Bienvenido a irrelevant club. No es una plataforma. No es un empresa tradicional de tecnologia. Es un club para gente que está cansada de hacer las cosas como "siempre se han hecho".

Por meses nos hemos preguntado: ¿Como podemos multiplicar 10X las habilidades y la productividad de nuestros usuarios? ¿Por qué seguimos haciendo con las uñas lo que otro hacen con tecnologia?

irrelevant nació para cambiar eso.

Lo que acabas de desbloquear:

→ Arsenal de herramientas tech que usamos a diario
→ Flujos de automatización que parecen magia negra
→ Recursos y código que nadie más comparte

Accede a todo con la frase secreta: "soy irrelevant club"

¿Necesitas algo a medida para tu empresa o equipo? Agenda una consulta: https://calendly.com/jpgomez-stayirrelevant/irrelevant-club?month=2025-03

Nos vemos del otro lado,
Equipo irrelevant

P.D. Si te preguntas si esto es para ti: si llegaste hasta aquí, lo es.

© {current_year} irrelevant. Todos los derechos reservados.
"""

def get_welcome_email_html(user_data, current_year):
    """
    Genera el HTML para el correo de bienvenida.

    Args:
        user_data (dict): Datos del usuario
        current_year (int): Año actual para el footer

    Returns:
        str: HTML del correo
    """
    return f"""<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bienvenido a irrelevant club</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        body {{
            font-family: 'Inter', sans-serif;
            margin: 0;
            padding: 0;
            background-color: #f5f5f5;
            color: #333;
            line-height: 1.5;
        }}
        .container {{
            max-width: 600px;
            margin: 0 auto;
            background-color: #14121f;
            border-radius: 16px;
            overflow: hidden;
            color: #e1e1e6;
        }}
        .header {{
            background: linear-gradient(125deg, #9C6BFF, #7A4FD3);
            padding: 30px 20px;
            text-align: center;
        }}
        .header img {{
            max-width: 180px;
            margin-bottom: 15px;
        }}
        .header h1 {{
            margin: 0;
            font-size: 28px;
            color: white;
            letter-spacing: -0.5px;
            font-weight: 800;
        }}
        .content {{
            padding: 35px 25px;
        }}
        .welcome-message {{
            margin-bottom: 30px;
            font-size: 16px;
        }}
        .welcome-message p {{
            margin-bottom: 18px;
        }}
        .manifesto {{
            background-color: #FFFFFF;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 35px;
            position: relative;
            overflow: hidden;
        }}
        .manifesto:before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, #9C6BFF, #7A4FD3);
        }}
        .manifesto p {{
            margin-bottom: 15px;
            font-size: 15px;
            line-height: 1.6;
        }}
        .manifesto p:last-child {{
            margin-bottom: 0;
        }}
        .arsenal-section {{
            margin: 35px 0;
        }}
        .arsenal-section h2 {{
            margin-bottom: 20px;
            font-size: 20px;
            color: white;
            display: flex;
            align-items: center;
            font-weight: 700;
        }}
        .arsenal-section h2 span {{
            color: #9C6BFF;
            margin-right: 8px;
            font-size: 24px;
        }}
        .tool-list {{
            list-style: none;
            padding: 0;
            margin: 0;
        }}
        .tool-list li {{
            position: relative;
            padding-left: 28px;
            margin-bottom: 15px;
            color: #b4b4b4;
            display: flex;
            align-items: center;
        }}
        .tool-list li:before {{
            content: attr(data-icon);
            position: absolute;
            left: 0;
            font-size: 16px;
        }}
        .secret-key {{
            background-color: #292841;
            border-radius: 12px;
            padding: 20px;
            text-align: center;
            border: 1px dashed #7A4FD3;
            position: relative;
            margin-top: 40px;
            margin-bottom: 40px;
        }}
        .secret-key:before {{
            content: '👁️ ACCESO';
            position: absolute;
            top: -12px;
            left: 50%;
            transform: translateX(-50%);
            background-color: #9C6BFF;
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            color: white;
        }}
        .secret-key p {{
            margin: 0 0 10px 0;
            color: #b4b4b4;
            font-size: 14px;
        }}
        .secret-key code {{
            display: block;
            background-color: #14121f;
            padding: 15px;
            border-radius: 8px;
            color: #9C6BFF;
            font-size: 18px;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-top: 15px;
        }}
        .special-box {{
            background-color: rgba(156, 107, 255, 0.1);
            border-radius: 12px;
            padding: 25px;
            margin: 35px 0;
            text-align: center;
        }}
        .special-box h3 {{
            margin-top: 0;
            margin-bottom: 15px;
            font-size: 18px;
            color: white;
        }}
        .special-box p {{
            margin-bottom: 20px;
            color: #b4b4b4;
            font-size: 15px;
        }}
        .cta-button {{
            display: inline-block;
            background: linear-gradient(to right, #9C6BFF, #7A4FD3);
            color: white;
            text-align: center;
            padding: 12px 25px;
            border-radius: 8px;
            text-decoration: none;
            font-weight: 600;
            font-size: 15px;
            transition: all 0.3s;
        }}
        .signature {{
            margin-top: 40px;
            font-size: 16px;
            color: white;
        }}
        .signature-name {{
            font-weight: 600;
            color: #9C6BFF;
        }}
        .postscript {{
            margin-top: 30px;
            font-style: italic;
            color: #9C6BFF;
            font-size: 14px;
            border-top: 1px solid #292841;
            padding-top: 20px;
        }}
        .footer {{
            background-color: #12101a;
            padding: 25px;
            text-align: center;
            font-size: 13px;
            color: #8e8e96;
        }}
        .social-links {{
            margin: 15px 0;
        }}
        .social-icon {{
            display: inline-block;
            width: 32px;
            height: 32px;
            background-color: #1c1a2e;
            border-radius: 50%;
            margin: 0 5px;
            line-height: 32px;
            text-align: center;
            color: #9C6BFF;
            text-decoration: none;
            font-size: 16px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <img src="https://storage.googleapis.com/cluvi/nuevo_irre-removebg-preview.png" alt="irrelevant Logo" />
            <h1>Bienvenido al Crew</h1>
        </div>
        <div class="content">
            <div class="welcome-message">
                <p>Hola <strong>{user_data['name']}</strong>,</p>
                <p style="color: white;">Bienvenido a irrelevant club. No es una plataforma. No es un empresa tradicional de tecnologia. Es un club para gente que está cansada de hacer las cosas como "siempre se han hecho"..</p>
            </div>
            <div class="arsenal-section">
                <h2><span>⚡</span> Lo que acabas de desbloquear:</h2>
                <ul class="tool-list">
                    <li>1. Arsenal de herramientas tech que usamos a diario y que multiplican nuestra capacidad</li>
                    <li>2. Flujos de automatización que parecen magia (y que nos tomó meses perfeccionar)</li>
                    <li>3. Tech stack, plugins y recursos que hemos recopilado obsesivamente</li>
                    <li>4. Comunidad de aprendizaje continuo sobre herramientas Tech, AI y Business</li>
                </ul>
            </div>
            <div class="secret-key">
                <p>Accede a todo con la frase secreta:</p>
                <code>soy irrelevant club</code>
            </div>
            <div class="special-box">
                <h3>¿Necesitas algo a medida para tu empresa?</h3>
                <p>Si quieres llevar esto al siguiente nivel y crear automatizaciones personalizadas para tu equipo, podemos hablar.</p>
                <a href="https://calendly.com/jpgomez-stayirrelevant/irrelevant-club?month=2025-03" class="cta-button">Agendar una consulta</a>
            </div>
            <div class="signature">
                <span style="color: white;">Let's Build The Future Together</span> 🚀<br>
                <span class="signature-name">Equipo irrelevant</span>
            </div>
            <div class="postscript">
                P.D. Si te preguntas si esto es para ti: si llegaste hasta aquí, lo es.
            </div>
        </div>
        <div class="footer">
            <div class="social-links">
                <a href="https://linkedin.com/company/irrelevant" class="social-icon">in</a>
                <a href="https://tiktok.com/@irrelevant" class="social-icon" style="font-size: 14px;">TT</a>
                <a href="https://youtube.com/c/irrelevant" class="social-icon" style="font-size: 14px;">YT</a>
            </div>
            <p>© {current_year} irrelevant. Todos los derechos reservados.</p>
        </div>
    </div>
</body>
</html>"""