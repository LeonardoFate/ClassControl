import paho.mqtt.client as mqtt

# Parámetros del broker MQTT
broker = "localhost"
port = 1883
base_topic = "asistencia/dia/#"  # Escuchar todos los tópicos de asistencia por día

# Función que maneja la recepción de mensajes
def on_message(client, userdata, msg):
    print(f"Mensaje recibido en el tópico {msg.topic}:")
    print(f"Contenido:\n{msg.payload.decode('utf-8')}")

# Crear cliente MQTT y especificar el protocolo MQTT v3.1.1
client = mqtt.Client("SuscriptorAsistencia", protocol=mqtt.MQTTv311)

# Conectar al broker MQTT
client.connect(broker, port)

# Configurar el manejador de mensajes
client.on_message = on_message

# Suscribirse al tópico de asistencia
client.subscribe(base_topic)

# Mantener el cliente funcionando para recibir los datos
client.loop_forever()
