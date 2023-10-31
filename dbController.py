import sqlite3

# подключение к базе данных
connect = sqlite3.connect("db.db")
cursor = connect.cursor()

# создание таблиц базы данных и связей
cursor.execute('''
CREATE TABLE IF NOT EXISTS  "users" ("id"	Integer not null, "login" Text not null, "password"	Text not null, PRIMARY KEY("id" AUTOINCREMENT));
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS  "type_links" ("id"	Integer not null, "name" Text not null, PRIMARY KEY("id" AUTOINCREMENT));
''')

cursor.execute('''
    CREATE TABLE IF NOT EXISTS "links" (
    "id" Integer not null, 
    "link" Text not null, 
    "user_id",
    "type_id" Integer not null,
    "short_link" Text not null,
    "count" Integer,
    PRIMARY KEY("id" AUTOINCREMENT)
    FOREIGN KEY (user_id)  REFERENCES users (id),
    FOREIGN KEY (type_id)  REFERENCES link_types (id)
);
''')

def setTypes(arr):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    for i in arr:
        cursor.execute('''INSERT INTO type_links('name') VALUES(?);''', (i,))
        print(i)
    connect.commit()

def getTypes():
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    return cursor.execute('SELECT * FROM type_links').fetchall()

def getLogin(login):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    return cursor.execute('SELECT id FROM users WHERE login = ?',(login,)).fetchone()
def getPsev(psev):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    return cursor.execute('SELECT link FROM links WHERE short_link = ?',(psev,)).fetchone()

def getTypebyLink(link):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    return cursor.execute('SELECT type_id FROM links WHERE link = ?',(link,)).fetchone()

def updateCounfLink(link):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    cursor.execute("UPDATE links SET count = count+1 WHERE link = ?", (link, ))
    connect.commit()

def getPass(login, passw):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    return cursor.execute('SELECT password FROM users WHERE login = ? AND password = ?',(login, passw)).fetchone()

def insertLink(link, us_id, type_id, short_l):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO links(link, user_id, type_id, short_link, count) VALUES(?,?,?,?, 0);''', (link, us_id, type_id, short_l,))
    connect.commit()

def insertLinkNotAuth(link,type_id, short_l):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO links(link, user_id, type_id, short_link, count) VALUES(?, NULL, ?, ?, 0);''', (link, type_id, short_l,))
    connect.commit()

def insertUser(login, password):
    connect = sqlite3.connect("db.db")
    cursor = connect.cursor()
    cursor.execute('''INSERT INTO users(id, login, password) VALUES(NULL, ?,?);''', (login, password,))
    connect.commit()

# types = ["Публичная", "Общего доступа", "Приватная"]
# setTypes(types)
connect.commit()