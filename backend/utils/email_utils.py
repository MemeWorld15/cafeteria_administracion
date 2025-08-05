import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
import os

load_dotenv()

EMAIL_ADDRESS = os.getenv("SMTP_EMAIL")
EMAIL_PASSWORD = os.getenv("SMTP_PASSWORD")

def enviar_correo_recuperacion(destinatario, enlace):
    msg = EmailMessage()
    msg['Subject'] = 'Recuperación de contraseña'
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = destinatario
    msg.set_content(f"""
Hola,

Recibimos una solicitud para restablecer tu contraseña.

Haz clic en el siguiente enlace para establecer una nueva contraseña:

{enlace}

Si no solicitaste este cambio, puedes ignorar este mensaje.

Saludos,
Cafetería
""")

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        smtp.send_message(msg)
