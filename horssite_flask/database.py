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
    cur.execute("SELECT * FROM mainmenu")
    menu = cur.fetchall()
    return menu


@database_connection
def add_posts(cur, title, text, time):
    cur.execute("INSERT INTO posts(title, text, time) VALUES(%s, %s, %s)",
                 (title, text, time))
