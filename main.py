from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session
from dbController import *
import random
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'xyijagjigfiljgfjioagojgraijosdftfghbhjngaoinjdhaih'




def Nav():
    if session.get("auth"):
        arr = [{"url":"/", "name": "Главная"},{"url":"/user", "name": session.get("login")}, {"url":"/logout", "name": "exit"}]
    else:
        arr = [{"url": "/", "name": "Главная"}, {"url": "/reg", "name": "Регистрация / Авторизация"}]
    return arr
def Types(arr):

    if session.get("auth"):
        types = []
        for i in arr:
            types.append({"id_type": i[0], "type": i[1]})
    else:

        types = [{"id_type": 1, "type": "Публичная"}]

    return types

#заполнение типов если пусто
if not getTypes():
    types = ["Публичная", "Общего доступа", "Приватная"]
    setTypes(types)

@app.route('/')
def index():
    arr = getTypes()
    return render_template('index.html', nav = Nav(), types=Types(arr))

@app.route('/auth')
def auth():
    return render_template('auth.html', nav = Nav())

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('auth', None)
    return redirect('/', code = 302)

@app.route('/reg')
def reg():
    return render_template('regestr.html', nav = Nav())


@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':

        login = request.form['login']
        passw = request.form['cpass']
        password = request.form['pass']
        print(getLogin(login))
        if(getLogin(login) == None):
            print("insert fffff")
            print(passw)
            print(password)
            if passw == password:
                insertUser(login,password)
                id_user = getLogin(login)
                session["user_id"] = id_user[0]
                session["login"] = login
                session["auth"] = True

                return redirect('/', code = 302)
            else:

                flash("Пароли не совпадают")
                return redirect('/reg', code = 302)
        else:
            flash("Логин занят")
            return redirect('/reg', code=302)

@app.route('/memberlogin', methods=['POST'])
def memberlogin():
    if request.method == 'POST':
        login = request.form['login']
        passw = request.form['pass']
        print(getLogin(login))
        if(getLogin(login) != None):
            passwUser = getPass(login, passw)
            passwUser = passwUser[0]

            if passwUser == passw:
                session["login"] = login
                session["auth"] = True
                id_user = getLogin(login)
                session["user_id"] = id_user[0]

                return redirect('/', code = 302)
            else:
                flash("Пароль неверный")
                return redirect('/auth', code = 302)
        else:
            flash("Логин неверный")
            return redirect('/auth', code = 302)

    else:
        flash("Метод")
        return redirect('/auth', code = 302)

if __name__ == '__main__':
    app.run(debug=True)