import cv2
import dlib
import numpy as np
import sqlite3
import os
from datetime import datetime

# Ruta al archivo de modelo preentrenado de dlib
predictor_path = '/home/Proyect/Desktop/AppClass/shape_predictor_68_face_landmarks.dat'
face_rec_model_path = '/home/Proyect/Desktop/AppClass/dlib_face_recognition_resnet_model_v1.dat'

# Cargar el detector de rostros y el predictor de puntos faciales
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor(predictor_path)
face_recognizer = dlib.face_recognition_model_v1(face_rec_model_path)

# Conectar a la base de datos SQLite para obtener las imágenes de los usuarios registrados
db_path = '/home/Proyect/Desktop/AppClass/backend/db.sqlite3'
conn = sqlite3.connect(db_path)
c = conn.cursor()

# Obtener todos los usuarios registrados (nombre y ruta de la imagen)
c.execute("SELECT nombre, foto FROM estudiantes")
registered_users = c.fetchall()

# Lista para almacenar las codificaciones faciales y los nombres asociados
known_face_encodings = []
known_face_names = []

# Cargar cada imagen registrada y calcular su codificación facial
for user in registered_users:
    name, img_path = user
    img_path = os.path.join('/home/Proyect/Desktop/AppClass/backend/', img_path)
    
    registered_image = cv2.imread(img_path)
    if registered_image is None:
        print(f"Error: No se pudo cargar la imagen en la ruta {img_path}.")
        continue

    registered_gray = cv2.cvtColor(registered_image, cv2.COLOR_BGR2GRAY)
    faces_in_registered_image = detector(registered_gray)
    
    if len(faces_in_registered_image) == 0:
        print(f"No se detectaron rostros en la imagen {img_path}.")
        continue
    
    shape = predictor(registered_gray, faces_in_registered_image[0])
    registered_face_encoding = np.array(face_recognizer.compute_face_descriptor(registered_image, shape))
    
    known_face_encodings.append(registered_face_encoding)
    known_face_names.append(name)

# Iniciar la captura de video en tiempo real desde la cámara
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        print("Error al capturar el video.")
        break

    # Convertir el cuadro a escala de grises y detectar rostros
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces_in_frame = detector(gray_frame)

    for face in faces_in_frame:
        # Obtener los puntos faciales y calcular la codificación facial
        shape = predictor(gray_frame, face)
        face_encoding = np.array(face_recognizer.compute_face_descriptor(frame, shape))

        # Comparar la codificación con todas las codificaciones registradas
        distances = np.linalg.norm(known_face_encodings - face_encoding, axis=1)
        min_distance_index = np.argmin(distances)
        
        if distances[min_distance_index] < 0.6:  # 0.6 es un umbral común para la coincidencia
            name = known_face_names[min_distance_index]
            
            # Obtener la fecha actual
            fecha = datetime.now().strftime("%Y-%m-%d")

            # Verificar si ya existe un registro para este usuario y esta fecha
            c.execute("SELECT * FROM asistencia WHERE nombre = ? AND fecha = ?", (name, fecha))
            resultado = c.fetchone()

            if resultado is None:
                # Registrar la asistencia si no existe un registro para hoy
                hora = datetime.now().strftime("%H:%M:%S")
                c.execute("INSERT INTO asistencia (nombre, fecha, hora) VALUES (?, ?, ?)", (name, fecha, hora))
                conn.commit()

        else:
            name = "Desconocido"

        # Dibujar un cuadro alrededor del rostro y mostrar el nombre
        x, y, w, h = (face.left(), face.top(), face.width(), face.height())
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(frame, name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

    # Mostrar el video en tiempo real con las detecciones
    cv2.imshow('Reconocimiento Facial en Tiempo Real', frame)

    # Presionar 'q' para salir
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar recursos
cap.release()
cv2.destroyAllWindows()

# Cerrar la conexión con la base de datos
conn.close()
