
from flask import render_template
from application import app, tweetry_manager

@app.route('/')
def index():
    return render_template('index.html', tweetry=tweetry_manager.tweetry)