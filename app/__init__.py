from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from datetime import timedelta
from app.db_connect import connect

app = Flask(__name__)
app.config.from_object(Config)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://admin:Bluehorse7@sgarrett-4214-practice.c2e1dpbmjmfg.us-east-2.rds.amazonaws.com/sys'

app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=120)
db = SQLAlchemy(app)

login = LoginManager(app)

from app import routes, models

if __name__ == '__main__':
    app.run(debug=True)