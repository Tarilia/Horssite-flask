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
    except:
        print("Ошибка чтения из БД")
    return []


@database_connection
def add_posts(cur, title, text, time):
    try:
        cur.execute("INSERT INTO posts(title, text, time) VALUES(%s, %s, %s)",
                    (title, text, time))
    except:
        print("Ошибка добавления статьи в БД ")
        return False


@database_connection
def get_post(cur, post_id):
    try:
        cur.execute(f"SELECT title, text FROM posts WHERE id = {post_id} LIMIT 1")
        result = cur.fetchone()
        if result:
            return result
    except:
        print("Ошибка добавления статьи из БД ")
        return False, False


@database_connection
def get_all_posts(cur):
    try:
        cur.execute("SELECT id, title, text FROM posts ORDER BY time DESC")
        result = cur.fetchall()
        return result
    except:
        print("Ошибка получения статьи из БД ")
    return []


@database_connection
def add_user(cur, name, email, psw, time):
    try:
        cur.execute("INSERT INTO users(name, email, psw, time) VALUES(%s, %s, %s, %s)",
                    (name, email, psw, time,))
    except:
        print("Ошибка добавления пользователя в БД ")
        return False
    return True
