import paho.mqtt.client as mqtt
from datetime import datetime
import sqlite3

# Ruta a tu base de datos SQLite
db_path = "/home/Proyect/Desktop/AppClass/backend/db.sqlite3"

# Función para obtener los registros de asistencia del día actual
def obtener_asistencia_del_dia():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    query = "SELECT nombre, fecha, hora FROM asistencia WHERE fecha = ?"
    cursor.execute(query, (fecha_hoy,))
    registros = cursor.fetchall()
    conn.close()
    return registros

# Parámetros del broker MQTT
broker = "localhost"
port = 1883
base_topic = "asistencia/dia"

# Función para publicar la asistencia o un mensaje cuando no haya registros
def publicar_asistencia(asistencia):
    client = mqtt.Client("PublicadorAsistencia")
    client.connect(broker, port)

    fecha_hoy = datetime.now().strftime("%Y-%m-%d")
    topic = f"{base_topic}/{fecha_hoy}"

    if not asistencia:
        # Publicar un mensaje de "sin asistencia"
        contenido = "No hubo asistencias registradas para hoy."
        print(f"Publicado en el tópico {topic}:\n{contenido}")
    else:
        # Publicar los registros de asistencia
        contenido = "\n".join([f"{nombre}, {fecha}, {hora}" for nombre, fecha, hora in asistencia])
        print(f"Publicado en el tópico {topic}:\n{contenido}")

    client.publish(topic, contenido)
    client.disconnect()

# Extraer y publicar la asistencia del día actual
asistencia_hoy = obtener_asistencia_del_dia()
publicar_asistencia(asistencia_hoy)
