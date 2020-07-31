

# TweetryDish

TweetryDish is a Flask web application that allows users to vote and modify each word of a daily quote. 
Each day the quote is automatically tweeted with the highest voted words for that day.  The app is hosted on
Heroku and can be found at https://tweetry-dish-app.herokuapp.com/.

![tweetry-dish](https://user-images.githubusercontent.com/33850990/88748945-e2569700-d117-11ea-8278-4c2492034b2a.gif)

![image](https://user-images.githubusercontent.com/33850990/88752271-200aee00-d11f-11ea-9f02-e802a0acb822.png)

- [Setup](#setup)
- [Commands](#commands)
- [Built With](#built-with)

## Setup

If you'd like to get the project running locally start by setting up .git in a new folder:
```
git init
```

Pull the repo into the folder:
```
git pull https://github.com/djleedke/tweetry-dish-app.git
```

Install virtualenv if you don't have it already and set up the environment (in the root folder still): 
```
pip install virtualenv
```
```
python -m virtualenv venv
```

Activate the virtual environment:
```
venv\scripts\activate
```

Now install the requirements.txt packages:
```
pip install -r requirements.txt
```

Now that the basic environment is set up there are a few other items to consider. The first being that you will need to create a keys.py file
to hold your Twitter API keys.  You will need to sign up for a development account w/ Twitter which you can do [here](https://developer.twitter.com/en).  

Create keys.py in the root folder and then add the following:
```
api_key = 'YOUR API KEY'
api_secret_key = 'YOUR API SECRET KEY'

access_token = 'YOUR ACCESS TOKEN'
access_token_secret = 'YOUR ACCESS TOKEN SECRET'
```

Once this is done you should be able to get the server started, set your FLASK_APP environment variable (for Windows):
```
set FLASK_APP=run.py
```
Now run the app:
```
flask run
```

At this point the server should run but you will get an error when accessing local host in the browser (Navigate to 127.0.0.1:5000 or localhost:5000 in the browser to verify). 
We need to set up the database and initialize a few things, run the following command:
```
flask create_tables
```
This will create all of the tables the app needs to run, load up the database with quotes from quotes.py, and create the first tweetry.  It's worth noting that 
the app at this point is using SQLite as the database. You will see a site.db file that was created automatically in the application folder.  In production it is using
Postgres on Heroku but this may vary depending on where it is deployed.

If you head back to 127.0.0.1:5000 in the browser you should now see things running correctly.  Congrats!  If you would like to turn on the scheduler (which handles the tweeting), open a new command prompt from the root folder with the virtual environment active and enter:
```
python scheduler.py
```
It's default setting is to finalize the tweet at 12:00am UTC each day but you can easily change this in scheduler.py if you'd like.  At that time the tweet will post, and a new tweetry will be created with a new quote.  The quote will not automatically change on it's own unless the scheduler is active nor will it tweet anything.  If you'd like to manually change the quote, use the `flask create_new_tweetry` command to do so.  


## Commands

Creates tables, loads new quotes, and initializes the first Tweetry:
```
flask create_tables
```

Drops all tables (WARNING: All data will be lost!):
```
flask drop_tables
```

Creates a new Tweetry and sets it to active, the old Tweetry will still exist in the database:
```
flask create_new_tweetry
```

Checks quotes.py for new quotes and then adds them to the database:
```
flask check_quotes
```

## Built With

- [Flask](https://flask.palletsprojects.com/en/1.1.x/) - for the webserver
- [SQLAlchemy](https://www.sqlalchemy.org/) - for handling the database
- [Tweepy](http://docs.tweepy.org/en/latest/) - for tweeting
- [APScheduler](https://apscheduler.readthedocs.io/en/stable/) - for scheduling the tweet event
- [Datamuse API](https://www.datamuse.com/api/) - for the word search functionality
- [Heroku](https://dashboard.heroku.com/) - for deployment


