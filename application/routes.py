
from flask import render_template
from application import app, quote_manager

@app.route('/')
def index():
    return render_template('index.html', current_quote=quote_manager.current_quote)