from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app) 

from application.tweetry_manager import TweetryManager
tweetry_manager = TweetryManager()

from application import scheduler
from application import routes


