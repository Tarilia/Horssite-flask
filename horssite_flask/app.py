from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from dotenv import load_dotenv
import os
import math
import time

from horssite_flask.database import get_menu, add_posts, get_post


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    menu = get_menu()
    return render_template('index.html', menu=menu)


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
    title, post = get_post(id_post)
    if not title:
        abort(404)
    return render_template('post.html', menu=menu, title=title, post=post)
