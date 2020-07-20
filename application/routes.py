
from flask import render_template, request, jsonify
from application import app, tweetry_manager
from application import app

@app.route('/')
def index():

    data = {
        'tweetry' : tweetry_manager.get_current_tweetry()
    }

    #tweetry_manager.tweet_final_quote()

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

@app.route('/refresh-quote-words', methods=['GET', 'POST'])
def top_choice_for_words():
    if request.method == 'POST': 
        return jsonify(tweetry_manager.get_top_choice_for_words(request.get_json()))
    else:
        return 'Failed'

@app.route('/refresh-top-choice-list', methods=['GET', 'POST'])
def top_choices():
    
    if request.method == 'POST': 
        return tweetry_manager.get_top_choice_list(request.get_json())
    else:
        return 'Failed'
