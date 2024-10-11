from flask import Flask, render_template, request, jsonify, make_response
import mysql.connector
import datetime

app = Flask(__name__)

con = mysql.connector.connect(
    host="185.232.14.52",
    database="u760464709_tst_sep",
    user="u760464709_tst_sep_usr",
    password="dJ0CIAFF="
)

@app.route("/")
def index():
    return render_template("app.html")

@app.route("/buscar")
def buscar():
    if not con.is_connected():
        con.reconnect()

    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id, Nombre, Email FROM usuarios ORDER BY Id DESC")
    usuarios = cursor.fetchall()
    con.close()

    return jsonify(usuarios)

@app.route("/guardar", methods=["POST"])
def guardar():
    if not con.is_connected():
        con.reconnect()

    id = request.form.get("id")
    nombre = request.form["nombre"]
    email = request.form["email"]

    cursor = con.cursor()

    if id:
        sql = "UPDATE usuarios SET Nombre=%s, Email=%s WHERE Id=%s"
        val = (nombre, email, id)
    else:
        sql = "INSERT INTO usuarios (Nombre, Email) VALUES (%s, %s)"
        val = (nombre, email)

    cursor.execute(sql, val)
    con.commit()
    con.close()

    return make_response(jsonify({}))

@app.route("/editar", methods=["GET"])
def editar():
    if not con.is_connected():
        con.reconnect()

    id = request.args["id"]
    cursor = con.cursor(dictionary=True)
    cursor.execute("SELECT Id, Nombre, Email FROM usuarios WHERE Id=%s", (id,))
    usuario = cursor.fetchone()
    con.close()

    return jsonify(usuario)

@app.route("/eliminar", methods=["POST"])
def eliminar():
    if not con.is_connected():
        con.reconnect()

    id = request.form["id"]
    cursor = con.cursor()
    cursor.execute("DELETE FROM usuarios WHERE Id=%s", (id,))
    con.commit()
    con.close()

    return jsonify({})
