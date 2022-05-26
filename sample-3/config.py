from __main__ import app
from flask_pymongo import PyMongo

def get_db_questions_connection():
    app.config["MONGO_URI"] = "mongodb://localhost:27017/databasename"
    mongo = PyMongo(app)
    return mongo.db.questions

def get_db_answers_connection():
    app.config["MONGO_URI"] = "mongodb://localhost:27017/databasename"
    mongo = PyMongo(app)
    return mongo.db.answers
