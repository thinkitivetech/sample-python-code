from flask import Flask
from .database import init_db
app = Flask(__name__)
app.config['SECRET_KEY'] = 'the random string'

init_db()

from app import views
from app import admin_views
