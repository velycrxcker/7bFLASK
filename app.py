from flask import Flask, render_template, request, jsonify
import pusher
import mysql.connector
import datetime
import pytz

# Conexión a la base de datos
con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/registro")
def registro():
    return render_template("registro-usuario.html")

@app.route("/buscar_usuarios")
def buscar_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario, Contraseña FROM tst0_usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()
    con.close()

    # Convertir registros a un formato más fácil de usar
    usuarios = [{"Id_Usuario": row[0], "Nombre_Usuario": row[1], "Contraseña": row[2]} for row in registros]
    return jsonify(usuarios)  # Enviar respuesta como JSON

@app.route("/usuarios/guardar", methods=["POST"])
def guardar_usuario():
    nombre_usuario = request.form["txtNombreUsuario"]
    contrasena = request.form["txtContrasena"]

    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor()
    sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contraseña) VALUES (%s, %s)"
    val = (nombre_usuario, contrasena)
    cursor.execute(sql, val)

    con.commit()
    con.close()

    return f"Usuario {nombre_usuario} guardado correctamente."

if __name__ == "__main__":
    app.run(debug=True)
