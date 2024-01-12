from flask import Flask, render_template, url_for, request, flash, session, redirect, abort
from dotenv import load_dotenv
import os

from horssite_flask.database import get_menu


load_dotenv()
app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    menu = get_menu()
    return render_template('index.html', menu=menu)
