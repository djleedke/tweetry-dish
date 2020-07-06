from flask import Flask, render_template
from quote_manager import QuoteManager

app = Flask(__name__)

quote_manager = QuoteManager()

@app.route('/')
def index():
    return render_template('index.html', current_quote=quote_manager.current_quote)