from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import os
import base64

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'images/'  # Asegúrate de que esta ruta sea relativa a 'backend'

def init_db():
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS estudiantes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                 nombre TEXT,
                 email TEXT,
                 foto TEXT)''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('register.html')

@app.route('/register', methods=['POST'])
def register():
    nombre = request.form['nombre']
    email = request.form['email']
    foto_data = request.form['foto']
    
    # Decodificar la imagen base64
    foto_data = foto_data.split(',')[1]  # Remover el encabezado 'data:image/png;base64,'
    foto_binary = base64.b64decode(foto_data)
    
    # Generar el nombre del archivo y guardarlo
    foto_filename = f"{nombre}.png"
    foto_path = os.path.join(app.config['UPLOAD_FOLDER'], foto_filename)
    
    try:
        with open(foto_path, 'wb') as f:
            f.write(foto_binary)
        print(f"Foto guardada en: {foto_path}")  # Mensaje de depuración
    except Exception as e:
        print(f"Error al guardar la foto: {e}")
    
    # Guardar la ruta de la foto en la base de datos
    db_path = os.path.join(os.path.dirname(__file__), 'db.sqlite3')
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute("INSERT INTO estudiantes (nombre, email, foto) VALUES (?, ?, ?)", (nombre, email, foto_path))
    conn.commit()
    conn.close()

    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
