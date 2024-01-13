import os
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv


load_dotenv()
DATABASE_URL = os.getenv('DATABASE_URL')


def database_connection(func):
    def wrapper(*args, **kwargs):
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor(cursor_factory=RealDictCursor)
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
