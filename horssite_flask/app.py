from flask import (Flask, render_template, url_for, make_response,
                   request, flash, session, redirect, abort)
from dotenv import load_dotenv
import os
import math
import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import (LoginManager, login_user, login_required, logout_user,
                         current_user)

from horssite_flask.admin.admin import admin
from horssite_flask.forms import LoginForm, RegisterForm
from horssite_flask.userlogin import UserLogin
from horssite_flask.database import (get_menu, add_posts, get_post,
                                     get_all_posts, add_user,
                                     get_email, update_avatar, update_posts,
                                     del_post)


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

app.register_blueprint(admin, url_prefix='/admin')

MAX_CONTENT_LENGTH = 1024 * 1024

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"


@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id)


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
            return redirect(url_for('index'))
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('add_post.html', menu=menu,
                           title="Добавление статьи")


@app.route("/post/<int:id_post>")
@login_required
def show_post(id_post):
    menu = get_menu()
    title = get_post(id_post)[0]
    post = get_post(id_post)[1]
    if not title:
        abort(404)
    return render_template('post.html', menu=menu, title=title, id_post=id_post, post=post)


@app.route("/post/<int:id_post>/update", methods=["POST", "GET"])
@login_required
def update_post(id_post):
    menu = get_menu()
    if request.method == "POST":
        name = request.form.get('name')
        post = request.form.get('post')
        tm = math.floor(time.time())
        if len(name) > 4 and len(post) > 10:
            update_posts(name, post, tm, id_post)
            return redirect(url_for('index'))
            flash('Статья добавлена успешно', category='success')
        else:
            flash('Ошибка добавления статьи', category='error')
    return render_template('update_post.html', menu=menu, title="Редактирование статьи")


@app.route("/post/<int:id_post>/delete")
@login_required
def delete_post(id_post):
    del_post(id_post)
    return redirect(url_for('index'))


@app.route("/login", methods=["POST", "GET"])
def login():
    menu = get_menu()
    if current_user.is_authenticated:
        return redirect(url_for('profile'))
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        psw = form.psw.data
        user = get_email(email)
        if user and check_password_hash(user['psw'], psw):
            userlogin = UserLogin().create(user)
            rm = form.remember.data
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or url_for("profile"))
        flash("Неверная пара логин/пароль", "error")
    return render_template("login.html", menu=menu, title="Авторизация", form=form)


@app.route("/register", methods=["POST", "GET"])
def register():
    menu = get_menu()
    form = RegisterForm()
    if form.validate_on_submit():
        tm = math.floor(time.time())
        email = form.email.data
        name = form.name.data
        psw = request.form.get('psw')
        hash = generate_password_hash(psw)
        result = add_user(name, email, hash, tm)
        if result:
            flash("Вы успешно зарегистрированы", "success")
            return redirect(url_for('login'))
        else:
            flash("Ошибка при добавлении в БД", "error")
    return render_template("register.html", menu=menu, title="Регистрация", form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('login'))


@app.route('/profile')
@login_required
def profile():
    menu = get_menu()
    return render_template("profile.html", menu=menu, title="Профиль")


@app.route('/userava')
@login_required
def userava():
    img = current_user.getAvatar(app)
    if not img:
        return ""
    get_img = make_response(img)
    get_img.headers['Content-Type'] = 'image/png'
    return get_img


@app.route('/upload', methods=["POST", "GET"])
@login_required
def upload():
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                res = update_avatar(img, current_user.get_id())
                if not res:
                    flash("Ошибка обновления аватара", "error")
                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла" + str(e), "error")
        else:
            flash("Ошибка обновления аватара", "error")
    return redirect(url_for('profile'))
