from flask import Flask, render_template, url_for, request

app = Flask(__name__)

menu = [{"name": "Главная", "url": "home"},
        {"name": "Добавить статью", "url": "add"},
        {"name": "Обратная связь", "url": "contact"},
        {"name": "Вход", "url": "entrance"}]


@app.route('/')
def index():
    return render_template('index.html', menu=menu)

