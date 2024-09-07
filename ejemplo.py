import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del correo electrónico para Outlook
smtp_server = 'smtp.office365.com'
smtp_port = 587
email_user = ''  # Tu correo de Outlook
email_password = ''  # Tu contraseña de Outlook
email_from = ''
email_to = ''
email_subject = 'Informe de Asistencia'

# Crear el mensaje de correo
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = email_subject

# Cuerpo del correo
body = "Aquí está el reporte de asistencia del día."
msg.attach(MIMEText(body, 'plain'))

# Enviar el correo
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Usar TLS para asegurar la conexión
    server.login(email_user, email_password)  # Iniciar sesión con las credenciales de Outlook
    server.sendmail(email_from, email_to, msg.as_string())  # Enviar el correo
    print("Correo enviado con éxito.")
    server.quit()  # Cerrar la conexión al servidor SMTP
except Exception as e:
    print(f"Error al enviar el correo: {e}")
