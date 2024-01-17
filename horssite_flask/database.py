import os
import psycopg2
from psycopg2.extras import DictCursor
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def database_connection(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=DictCursor)
        connection = func(cur, *args, **kwargs)
        conn.commit()
        conn.close()
        return connection
    return wrapper


@database_connection
def get_menu(cur):
    try:
        cur.execute("SELECT * FROM mainmenu")
        menu = cur.fetchall()
        return menu
    except Exception as error:
        print("Ошибка чтения из БД" + str(error))
    return []


@database_connection
def add_posts(cur, title, text, time):
    try:
        cur.execute("INSERT INTO posts(title, text, time) VALUES(%s, %s, %s)",
                    (title, text, time))
    except Exception as error:
        print("Ошибка добавления статьи в БД" + str(error))
        return False


@database_connection
def get_post(cur, post_id):
    try:
        cur.execute(f"SELECT title, text FROM posts \
                    WHERE id = {post_id} LIMIT 1")
        result = cur.fetchone()
        if result:
            return result
    except Exception as error:
        print("Ошибка добавления статьи из БД" + str(error))
        return False, False


@database_connection
def get_all_posts(cur):
    try:
        cur.execute("SELECT id, title, text FROM posts ORDER BY time DESC")
        result = cur.fetchall()
        return result
    except Exception as error:
        print("Ошибка получения статьи из БД" + str(error))
    return []


@database_connection
def add_user(cur, name, email, psw, time):
    try:
        cur.execute("INSERT INTO users(name, email, psw, time) \
                    VALUES(%s, %s, %s, %s)",
                    (name, email, psw, time,))
    except Exception as error:
        print("Ошибка добавления пользователя в БД" + str(error))
        return False
    return True


@database_connection
def get_user(cur, user_id):
    try:
        cur.execute(f"SELECT * FROM users WHERE id = {user_id} LIMIT 1", (user_id,))
        result = cur.fetchone()
        if result:
            return result
    except Exception as error:
        print("Ошибка получения данных из БД" + str(error))
    return False


@database_connection
def get_email(cur, email):
    try:
        cur.execute(f"SELECT * FROM users WHERE email = '{email}' LIMIT 1", (email,))
        result = cur.fetchone()
        if not result:
            print("Пользователь не найден")
            return False
        return result
    except Exception as error:
        print("Ошибка получения данных из БД" + str(error))
    return False


@database_connection
def update_avatar(cur, avatar, user_id):
    if not avatar:
        return False
    try:
        cur.execute(f"UPDATE users SET avatar = %s WHERE id = %s", (avatar, user_id))
    except Exception as error:
        print("Ошибка обновления аватара в БД:" + str(error))
        return False
    return True
