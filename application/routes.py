
from flask import render_template, request
from application import app, tweetry_manager

@app.route('/')
def index():

    data = {
        'tweetry' : tweetry_manager.get_current_tweetry()
    }

    return render_template('index.html', data=data)

@app.route('/save', methods=['GET', 'POST'])
def save():

    if request.method == 'POST':
        tweetry_manager.update_choices(request.get_json())

    return 'Saved'