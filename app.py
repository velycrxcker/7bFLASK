from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector

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
    # Cerrar la conexión si está abierta
    if con.is_connected():
        con.close()
    return render_template("registro-usuario.html")

@app.route("/usuarios/guardar", methods=["POST"])
def usuarios_guardar():
    # Reabrir conexión si está cerrada
    if not con.is_connected():
        con.reconnect()

    # Obtener datos del formulario
    nombre_usuario = request.form["txtUsuario"]
    contrasena = request.form["txtContrasena"]

    # Guardar en la base de datos
    cursor = con.cursor()
    sql = """
        INSERT INTO usuarios (Nombre_Usuario, Contrasena)
        VALUES (%s, %s)
    """
    val = (nombre_usuario, contrasena)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    # Respuesta
    return f"Usuario {nombre_usuario} registrado con éxito"

@app.route("/usuarios")
def listar_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("""
    SELECT Id_Usuario, Nombre_Usuario FROM usuarios
    """)
    usuarios = cursor.fetchall()
    con.close()

    return make_response(jsonify(usuarios))

if __name__ == "__main__":
    app.run(debug=True)
