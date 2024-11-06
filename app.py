from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

app = Flask(__name__)
CORS(app)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/buscar_usuarios")
def buscar_usuarios():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios ORDER BY Id_Usuario DESC")
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/guardar_usuario", methods=["POST"])
def guardar_usuario():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]
    nombre = request.form["nombre"]
    contrasena = request.form["contrasena"]

    cursor = con.cursor()

    if id:  # Si se proporciona un id, es una actualización
        sql = "UPDATE tst0_usuarios SET Nombre_Usuario = %s, Contrasena = %s WHERE Id_Usuario = %s"
        val = (nombre, contrasena, id)
    else:  # Si no hay id, es una inserción
        sql = "INSERT INTO tst0_usuarios (Nombre_Usuario, Contrasena) VALUES (%s, %s)"
        val = (nombre, contrasena)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

@app.route("/editar_usuario", methods=["GET"])
def editar_usuario():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id_Usuario, Nombre_Usuario, Contrasena FROM tst0_usuarios WHERE Id_Usuario = %s", (id,))
    registros = cursor.fetchall()
    con.close()

    return make_response(jsonify(registros))

@app.route("/eliminar_usuario", methods=["POST"])
def eliminar_usuario():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]

    cursor = con.cursor(dictionary=True)
    cursor.execute("DELETE FROM tst0_usuarios WHERE Id_Usuario = %s", (id,))
    con.commit()
    con.close()

    return make_response(jsonify({}))

if __name__ == "__main__":
    app.run(debug=True)
