
from flask import render_template, request, jsonify
from application import app, tweetry_manager

@app.route('/')
def index():

    data = {
        'tweetry' : tweetry_manager.get_current_tweetry()
    }

    return render_template('index.html', data=data)


#---------- AJAX -----------

@app.route('/save-vote', methods=['GET', 'POST'])
def save_vote():
    if request.method == 'POST':
        return tweetry_manager.save_vote(request.get_json(), request.remote_addr)
    else:
        return 'Failed'

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
