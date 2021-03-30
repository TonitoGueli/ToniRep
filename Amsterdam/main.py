import streamlit as st
from flask import Flask, render_template, redirect, url_for, request, session
from flask_mysql_connector import MySQL
import pymysql
from subprocess import call
import webbrowser as wb

app = Flask(__name__)

app.secret_key = "120395"

app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "anto1203"
app.config["MYSQL_DB"] = "amsterdamdb"

db = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    def getnombreusuario():
        mailaux = 'email_usuario_from' in request.form
        print("variable" + mailaux)
        return mailaux
    if request.method == 'POST':
        if ('email_usuario_form' in request.form) and ('password_usuario_form' in request.form):
            usuarios_email_py = request.form['email_usuario_form']
            usuarios_password_py = request.form['password_usuario_form']
            cursor = db.connection.cursor(pymysql.cursors.DictCursor)
            cursor.execute(
                "SELECT USUARIOS_EMAIL, USUARIOS_LOGIN_PASSWORD FROM amsterdamdb.usuarios WHERE USUARIOS_EMAIL=%s AND USUARIOS_LOGIN_PASSWORD=%s",
                (usuarios_email_py, usuarios_password_py))
            info = cursor.fetchone()
            if info is None:
                return redirect(url_for('registro'))
            else:
                if info[0] == usuarios_email_py and info[1] == usuarios_password_py:
                    session['loginsuccess'] = True
                    return redirect(url_for(home()))

    return render_template('./login.html')



@app.route('/register', methods=['GET', 'POST'])
def registro():
    if request.method == "POST":
        if "loginName" in request.form and "email" in request.form and "pass" in request.form and "pref1" in request.form and "pref2" in request.form and "pref3" in request.form and "fname" in request.form and "lname" in request.form and "dbirth" in request.form:
            usuarios_login_name_py = request.form['loginName']
            usuarios_email = request.form['email']
            usuarios_login_password_py = request.form['pass']
            usuarios_natural_name_py = request.form['fname']
            usuarios_natural_lastname1_py = request.form['lname']
            usuarios_preferencia1_py = request.form['pref1']
            usuarios_preferencia2_py = request.form['pref2']
            usuarios_preferencia3_py = request.form['pref3']
            usuarios_fecha_de_nacimiento_py = request.form['dbirth']
            cur = db.connection.cursor(pymysql.cursors.DictCursor)
            cur.execute(
                "INSERT INTO amsterdamdb.usuarios (usuarios_login_name, usuarios_login_password, usuarios_natural_name, usuarios_natural_lastname1, usuarios_preferencia_1,usuarios_preferencia_2, usuarios_preferencia_3, usuarios_email, usuarios_fecha_de_nacimiento) VALUES (%s, %s, %s,%s,%s,%s,%s,%s,%s)",
                (usuarios_login_name_py, usuarios_login_password_py, usuarios_natural_name_py,
                 usuarios_natural_lastname1_py, usuarios_preferencia1_py, usuarios_preferencia2_py,
                 usuarios_preferencia3_py, usuarios_email, usuarios_fecha_de_nacimiento_py))
            db.connection.commit()
            return redirect(url_for('index'))

    return render_template("register.html")


@app.route('/home')
def home():
    if session['loginsuccess'] == True:
        return redirect(url_for(call(["python", "iniciador.py"])))


@app.route('/logout')
def logout():
    session.pop('loginsuccess', None)
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)
