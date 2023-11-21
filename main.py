from flask import Flask, render_template, url_for, request, redirect, flash, get_flashed_messages, session, abort
from dbController import *
import hashlib
import string
import json
import random
from random import choice, randint

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = 'xyijagjigfiljgfjioagojgraijosdftfghbhjngaoinjdhaih'

def Nav():
    if session.get("auth"):
        arr = [{"url": "/", "name": "Главная"}, {"url": "/user", "name": session.get("login")}, {"url": "/logout", "name": "exit"}]
    else:
        arr = [{"url": "/", "name": "Главная"}, {"url": "/regestr", "name": "Регистрация / Авторизация"}]
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
    if session.get("auth") == None:
        session["auth"] = False
    arr = getTypes()
    return render_template('index.html', nav=Nav(), types=Types(arr))

@app.route('/auth')
def auth():
    return render_template('auth.html', nav=Nav())

@app.route('/noacces')
def noacces():
    return render_template('noacces.html', nav=Nav())

@app.route('/user')
def user():
    arr = getTypes()
    print(arr)
    links = getLinksByUser(session.get("user_id"))
    print(links)
    return render_template('user.html', nav=Nav(), links=links, types=Types(arr))

@app.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('link', None)
    session.pop('auth', None)
    return redirect('/', code = 302)
@app.route('/regestr')
def reg():
    return render_template('regestr.html', nav=Nav())

@app.route('/del', methods=['POST'])
def delete():
    print("delete")
    print(request.form['id'])
    if request.method == 'POST':
        link_id = request.form['id']
        deleteLink(link_id)
        return redirect('/user', code=302)
@app.route('/edit_psev', methods=['POST'])
def edit_psev():
    print("edit_psev")
    if request.method == 'POST':
        link_id = request.form['id']
        psev = request.form["psev"]
        if psev == '':
            host_url = request.host_url
            short_link = host_url + "link/" + ''.join(choice(string.ascii_letters + string.digits) for _ in range(randint(8, 12)))
            editPsevfLink(short_link, link_id)

            flash("Заполните псевдоним", category="error")
        else:
            new_link = request.host_url + "link/" + psev
            if getPsev(new_link) != None:
                flash("Псевдоним занят", category="error")
            else:
                editPsevfLink(new_link, link_id)
        return redirect('/user', code=302)

@app.route('/edit_type', methods=['POST'])
def edit_type():
    print("edit_type")
    if request.method == 'POST':
        link_id = request.form['id']
        type_id = request.form["type"]
        editTypefLink(type_id, link_id)
        return redirect('/user', code=302)
@app.route('/insert', methods=['POST'])
def insert():
    if request.method == 'POST':
        login = request.form['login']
        passw = request.form['cpass']
        password = request.form['pass']
        print(getLogin(login))
        if(login != '' and passw != '' and password != ''):
            if(getLogin(login) == None):
                if passw == password:
                    hashas = hashlib.md5(request.form["pass"].encode())
                    password = hashas.hexdigest()
                    insertUser(login, password)
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
        if (getLogin(login) != None):
            print(login)
            print(passw)
            hashas = hashlib.md5(request.form["pass"].encode())
            password = hashas.hexdigest()
            passwUser = getPass(login, password)

            if passwUser != None and passwUser[0] == password:
                session["login"] = login
                session["auth"] = True
                id_user = getLogin(login)
                session["user_id"] = id_user[0]
                if (session.get("link") != None):
                    return redirect(session.get("link"))
                else:
                    return redirect('/', code=302)
            else:
                flash("Пароль не тот")
                return redirect('/auth', code=302)
        else:
            flash("Логин не найден")
            return redirect('/auth', code=302)


@app.route('/createLink', methods=['POST'])
def linkCreate():
    if request.method == 'POST':
        host_url = request.host_url
        print(host_url)
        link = request.form['link']
        type = request.form['type']
        print(session.get("auth"))
        if link != "":
            if request.form.getlist('nik'):
                psev = request.form['psev']
                link_psev = host_url + "link/" + psev
                print(link_psev)
                print(getPsev(psev))
                if getPsev(link_psev) != None:
                    print(getPsev(psev))
                    flash("Выберите другой псевдоним, этот занят", category="error")
                else:
                    short_link = host_url + "link/" + psev
                    print("lin")
                    if session.get("auth"):
                        print("link")
                        insertLink(link, session.get("user_id"), type, short_link)
                    else:
                        insertLinkNotAuth(link, type, short_link)
                    flash(link, category="link")
                    flash(short_link, category="url")
            else:
                short_link = host_url + "link/" + ''.join(choice(string.ascii_letters + string.digits) for _ in range(randint(8, 12)))
                if session.get("auth"):
                    insertLink(link, session.get("user_id"), type, short_link);
                else:
                    insertLinkNotAuth(link, type, short_link)
                flash(link, category="link")
                flash(short_link, category="url")
        else:
            flash("Введите ссылку", category="error")
    # else:
    #     flash("Данная ссылка у вас уже есть", category="error")
    #     return redirect(request.host_url + 'links', code=302)
    return redirect("/", code=302)

#перенаправление ссылки
@app.route('/link/<short_link>')
def reassign_link(short_link):
    #dd = sqlite3.connect(r"database.db")
    #cursor = dd.cursor()
    user_link = request.host_url + "link/" + short_link
    uslink = getPsev(user_link)
    link = uslink[0]
    print(link)

    if link !=None:
        print(getTypebyLink(user_link))
        type = getTypebyLink(user_link)
        print(user_link)
        type_link = type[0]
        if type_link == 1:
            updateCounfLink(user_link)
            return redirect(link)
        else:
            session["link"] = user_link
            if session.get("auth"):
                if type_link == 2:
                    updateCounfLink(user_link)
                    session.pop('link', None)
                    return redirect(link)
                elif type_link == 3:
                    if session.get("user_id") == getUserbyLink(user_link)[0]:
                        updateCounfLink(user_link)
                        session.pop('link', None)
                        return redirect(link)
                    else:
                        session.pop('link', None)
                        return redirect('/noacces')
            else:
                return redirect("/auth")
    else:
        abort(404)


if __name__ == '__main__':
    app.run(debug=True)