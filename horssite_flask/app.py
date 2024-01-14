from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from dotenv import load_dotenv
import os
import math
import time
from werkzeug.security import generate_password_hash, check_password_hash

from horssite_flask.database import get_menu, add_posts, get_post, get_all_posts, add_user


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    menu = get_menu()
    posts = get_all_posts()
    return render_template('index.html', menu=menu, posts=posts)


@app.route("/add_post", methods=["POST", "GET"])
def add_post():
    menu = get_menu()
    if request.method == "POST":
        name = request.form.get('name')
        post = request.form.get('post')
        tm = math.floor(time.time())
        if len(name) > 4 and len(post) > 10:
            add_posts(name, post, tm)
            flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=menu, title="Добавление статьи")


@app.route("/post/<int:id_post>")
def show_post(id_post):
    menu = get_menu()
    title = get_post(id_post)[0]
    post = get_post(id_post)[1]
    if not title:
        abort(404)
    return render_template('post.html', menu=menu, title=title, post=post)


@app.route("/login", methods=["POST", "GET"])
def login():
    menu = get_menu()
    return render_template("login.html", menu=menu, title="Авторизация")


@app.route("/register", methods=["POST", "GET"])
def register():
    menu = get_menu()
    if request.method == "POST":
        tm = math.floor(time.time())
        name = request.form.get('name')
        email = request.form.get('email')
        psw = request.form.get('psw')
        psw2 = request.form.get('psw2')
        if len(name) > 4 and len(email) > 4 and len(psw) > 4 and psw == psw2:
            hash = generate_password_hash(psw)
            result = add_user(name, email, hash, tm)
            if result:
                flash("Вы успешно зарегистрированы", "success")
                return redirect(url_for('login'))
            else:
                flash("Ошибка при добавлении в БД", "error")
        else:
             flash("Неверно заполнены поля", "error")
    return render_template("register.html", menu=menu, title="Регистрация")
