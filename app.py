from flask import Flask, render_template, request, redirect, jsonify
import sqlite3

app = Flask(__name__)

# Conectar a la base de datos
def conectar_bd():
    conn = sqlite3.connect('usuarios.db')
    return conn

# Ruta principal para mostrar el formulario
@app.route('/')
def index():
    return render_template('registro-usuario.html')

# Ruta para registrar un usuario
@app.route('/registrar', methods=['POST'])
def registrar_usuario():
    nombre_usuario = request.form['nombre_usuario']
    contrasena = request.form['contrasena']

    conn = conectar_bd()
    cursor = conn.cursor()

    if request.form['id'] == '':  # Nuevo registro
        cursor.execute("INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (?, ?)", (nombre_usuario, contrasena))
    else:  # Actualizar registro existente
        id_usuario = request.form['id']
        cursor.execute("UPDATE tst0_usuarios SET Nombre_Usuario = ?, Contrasena = ? WHERE Id_Usuario = ?", (nombre_usuario, contrasena, id_usuario))

    conn.commit()
    conn.close()

    return redirect('/')

# Ruta para buscar usuarios
@app.route('/buscar', methods=['GET'])
def buscar_usuario():
    buscar_nombre = request.args.get('buscar_nombre', '')

    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario FROM tst0_usuarios WHERE Nombre_Usuario LIKE ?", ('%' + buscar_nombre + '%',))
    usuarios = cursor.fetchall()
    conn.close()

    return jsonify(usuarios)

# Ruta para eliminar un usuario
@app.route('/eliminar/<int:id>', methods=['POST'])
def eliminar_usuario(id):
    conn = conectar_bd()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM tst0_usuarios WHERE Id_Usuario = ?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
