from flask import Flask, render_template, url_for, request, flash, session, redirect, abort, g
from dotenv import load_dotenv
import os


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

menu = [{"name": "Главная", "url": "/"},
        {"name": "Добавить статью", "url": "add"},
        {"name": "Обратная связь", "url": "contact"},
        {"name": "Вход", "url": "entrance"}]


@app.route('/')
def index():
    return render_template('index.html', menu=menu)


@app.route('/contact', methods=["POST", "GET"])
def contact():
    if request.method == "POST":
        print(request.form['username'])
        if len(request.form['username']) > 2:
            flash('Сообщение отправлено', category='success')
        else:
            flash('Ошибка отправки', category='error')
    return render_template('contact.html', title="Обратная связь", menu=menu)
