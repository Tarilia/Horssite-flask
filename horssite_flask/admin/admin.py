from flask import (Blueprint, render_template, url_for,
                   redirect, session, request, flash)

from horssite_flask.admin.database_admin import get_list, get_users


admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

menu = [{'url': '.index', 'title': 'Панель'},
        {'url': '.listusers', 'title': 'Список пользователей'},
        {'url': '.listpubs', 'title': 'Список статей'},
        {'url': '.logout', 'title': 'Выйти'}]


def isLogged():
    return True if session.get('admin_logged') else False


def login_admin():
    session['admin_logged'] = 1


def logout_admin():
    session.pop('admin_logged', None)


@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.login'))
    return render_template('admin/index.html', menu=menu, title='Админ-панель')


@admin.route('/login', methods=["POST", "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "12345":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара логин/пароль", "error")
    return render_template('admin/login.html', title='Админ-панель')


@admin.route('/logout', methods=["POST", "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    logout_admin()
    return redirect(url_for('.login'))


@admin.route('/list-pubs')
def listpubs():
    if not isLogged():
        return redirect(url_for('.login'))
    list_post = get_list()
    return render_template('admin/listpubs.html', title='Список статей',
                           menu=menu, list=list_post)


@admin.route('/list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))
    list_users = get_users()
    return render_template('admin/listusers.html', title='Список пользователей',
                           menu=menu, list=list_users)
