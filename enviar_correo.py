import smtplib
import sqlite3
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Configuración del correo electrónico
smtp_server = 'smtp.office365.com'  # Servidor SMTP de Gmail
smtp_port = 587                 # Puerto SMTP para TLS
email_user = ''  # Tu correo de Gmail
email_password ='AndreLuz4554' #contraseña de Gmail o App Password si se usa 2FA
email_from = ''  # El mismo correo de Gmail
email_to =''  # Correo del destinatario 
email_subject = 'Informe de Asistencia'

# Conectar a la base de datos
db_path = '/home/Proyect/Desktop/AppClass/backend/db.sqlite3'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Obtener la fecha actual
fecha_hoy = datetime.now().strftime("%Y-%m-%d")

# Recuperar los registros de asistencia para la fecha actual
c.execute("SELECT nombre, fecha, hora FROM asistencia WHERE fecha = ?", (fecha_hoy,))
asistencia = c.fetchall()

# Cerrar la conexión con la base de datos
conn.close()

# Generar el cuerpo del correo electrónico
if asistencia:
    email_body = f"Informe de Asistencia para el {fecha_hoy}:\n\n"
    for registro in asistencia:
        nombre, fecha, hora = registro
        email_body += f"Nombre: {nombre}, Hora: {hora}\n"
else:
    email_body = f"No hay registros de asistencia para el {fecha_hoy}.\n"

# Crear el correo electrónico
msg = MIMEMultipart()
msg['From'] = email_from
msg['To'] = email_to
msg['Subject'] = email_subject

# Adjuntar el cuerpo del mensaje codificado en UTF-8
msg.attach(MIMEText(email_body, 'plain', 'utf-8'))

# Enviar el correo electrónico
try:
    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()  # Iniciar la conexión segura
    server.login(email_user, email_password)
    text = msg.as_string()
    server.sendmail(email_from, email_to, text.encode('utf-8'))
    server.quit()
    print(f"Informe de asistencia enviado a {email_to}.")
except Exception as e:
    print(f"Error al enviar el correo: {e}")
