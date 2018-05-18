from flask import Flask, render_template as render, request, redirect, url_for
from tinydb import TinyDB, Query, where

app = Flask(__name__)
db = TinyDB('db.json')
context = {'login': '', 'role':'guest', 'alert':''}

@app.route('/')
def index():
    context['alert'] = ''
    return render('index.html', **context)

@app.errorhandler(404)
def page_not_found(e):
    return render('err404.html')

@app.route('/testdb')
def testdb():
    User = Query()
    if len(db.search(User.login == 'admin')) == 0:
        db.insert({'login':'admin', 'email':'admin@ya.ru', 'password':'a'})
    if len(db.search(User.login == 'user')) == 0:
        db.insert({'login':'user', 'email':'user@ya.ru', 'password':'u'})
    return render('testdb.html', **context)

@app.route('/signin')
def signin():
    context['alert'] = ''
    return render('signin.html', **context)


@app.route('/signin', methods=['POST'])
def do_login():
    User = Query()
    users = db.search(User.login == request.form['login'])
    if len(users) > 0:
        user = users[0]
        print(user)
        print(user['password'], request.form['password'])
        if user['password'] == request.form['password']:
            context['login'] = user['login']
            context['role'] = 'admin'
            return render('index.html', **context)
        else:
            context['alert']='Неверный пароль'
    else:
        context['alert']='Пользователя с таким логином не существует'
    return render('signin.html', **context)


@app.route('/signout')
def logout():
    context['login'] = ''
    context['role'] = 'guest'
    return redirect('/')


@app.route('/signup')
def signup():
    return render('signup.html', **context)


@app.route('/signup', methods=['POST'])
def register():
    User = Query()
    users = db.search(User.login == request.form['login'])
    if len(users) > 0:
        context['alert'] = 'Пользователь с таким логином уже существует'
        return render('signup.html', **context)
    else:
        db.insert({
            'login' : request.form['login'],
            'email':request.form['password'],
            'password':request.form['password']
        })
      return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, port=8000)
