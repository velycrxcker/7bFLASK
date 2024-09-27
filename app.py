from flask import Flask, render_template, request
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
    return registros

if __name__ == "__main__":
    app.run(debug=True)
