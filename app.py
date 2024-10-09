from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Ruta principal para cargar la página del formulario de usuarios
@app.route("/")
def index():
    return render_template("app.html")

# Ruta para buscar usuarios en la tabla tst0_usuarios
@app.route("/buscar_usuarios")
def buscar_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Usuario, Nombre_Usuario, Contraseña FROM tst0_usuarios
    """)
    usuarios = cursor.fetchall()

    con.close()
    return make_response(jsonify(usuarios))

# Ruta para guardar o actualizar un usuario
@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id_usuario"]
    nombre_usuario = request.form["nombre_usuario"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()

    if id_usuario:  # Actualizar si existe un ID de usuario
        sql = """
        UPDATE tst0_usuarios SET
        Nombre_Usuario = %s,
        Contraseña = %s
        WHERE Id_Usuario = %s
        """
        val = (nombre_usuario, contrasena, id_usuario)
    else:  # Insertar nuevo usuario si no hay ID
        sql = """
        INSERT INTO tst0_usuarios (Nombre_Usuario, Contraseña)
        VALUES (%s, %s)
        """
        val = (nombre_usuario, contrasena)
    
    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

# Ruta para obtener los datos de un usuario específico y editarlos
@app.route("/editar_usuario", methods=["GET"])
def editar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.args["id"]

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Usuario, Nombre_Usuario, Contraseña FROM tst0_usuarios
    WHERE Id_Usuario = %s
    """, (id_usuario,))
    usuario = cursor.fetchall()
    con.close()

    return make_response(jsonify(usuario))

# Ruta para eliminar un usuario por su ID
@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    if not con.is_connected():
        con.reconnect()

    id_usuario = request.form["id"]

    cursor = con.cursor()
    cursor.execute("""
    DELETE FROM tst0_usuarios WHERE Id_Usuario = %s
    """, (id_usuario,))
    con.commit()
    con.close()

    return make_response(jsonify({}))

# Nueva ruta para buscar experiencias en la tabla tst0_experiencias
@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT Nombre_Apellido, Comentario, Calificacion FROM tst0_experiencias ORDER BY Id_Experiencia DESC")
    registros = cursor.fetchall()
    cursor.close()

    # Convertir los registros en una lista de diccionarios
    experiencias = [
        {
            "Nombre_Apellido": registro[0],
            "Comentario": registro[1],
            "Calificacion": registro[2]
        }
        for registro in registros
    ]
    return jsonify(experiencias)

# Iniciar la aplicación de Flask
if __name__ == "__main__":
    app.run(debug=True)
