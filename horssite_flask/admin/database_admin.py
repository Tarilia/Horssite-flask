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
def get_list(cur):
    try:
        cur.execute("SELECT id, title, text FROM posts ORDER BY time DESC")
        result = cur.fetchall()
        return result
    except:
        print("Ошибка получения статьи из БД")
    return []
