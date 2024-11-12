from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

# Ruta para obtener la lista de usuarios
@app.route("/usuarios", methods=["GET"])
def obtener_usuarios():
    if not con.is_connected():
        con.reconnect()
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios")
    usuarios = cursor.fetchall()
    return jsonify(usuarios)

# Ruta para agregar un nuevo usuario
@app.route("/usuarios", methods=["POST"])
def guardar_usuario():
    if not con.is_connected():
        con.reconnect()
    nombre = request.json["nombre"]
    contrasena = request.json["contrasena"]
    cursor = con.cursor()
    cursor.execute("INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)", (nombre, contrasena))
    con.commit()
    return jsonify({"message": "Usuario guardado"})

if __name__ == "__main__":
    app.run(debug=True)
