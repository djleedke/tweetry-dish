
from flask import render_template, request, jsonify
from application import app, tweetry_manager

@app.route('/')
def index():

    data = {
        'tweetry' : tweetry_manager.get_current_tweetry()
    }

    return render_template('index.html', data=data)


#---------- AJAX -----------

@app.route('/save-choice', methods=['GET', 'POST'])
def save_choice():

    if request.method == 'POST':
        tweetry_manager.update_choices(request.get_json())

    return 'Success'

@app.route('/top-choice', methods=['GET', 'POST'])
def top_choice():
    if request.method == 'POST': 
        return tweetry_manager.get_top_choice(request.get_json())
    else:
        return 'Failed'

@app.route('/top-choices', methods=['GET', 'POST'])
def top_choices():
    
    if request.method == 'POST': 
        return tweetry_manager.get_top_choices(request.get_json())
    else:
        return 'Failed'

