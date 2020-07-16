
from application.quotes import quotes
from application.models import Quote, Word, Tweetry, Choice
from application import db
import random, re

class TweetryManager:

    def __init__(self):
        print('Tweetry Manager: Initialized')
        self.check_for_new_quotes()
        self.create_new_tweetry()
        print(self.current_tweetry_id)

    #Create new tweetry and add to database
    def create_new_tweetry(self):
        tweetry = Tweetry(quote_id=random.randint(1, db.session.query(Quote).count()))
        db.session.add(tweetry)
        db.session.commit()
        self.voted_ips = []
        self.current_tweetry_id = tweetry.id
        return

    #Checks our quotes.py file to see if any new quotes have been added    
    def check_for_new_quotes(self):

        #Iterating over list of quotes in quotes.py
        for quote in quotes:

            #If we have come across a quote that did not exist we insert it
            if not Quote.query.filter_by(text=quote['text']).first():
                
                new_quote = Quote(author=quote['author'], text=quote['text'])
                db.session.add(new_quote)
                db.session.commit()
                
                #We also insert the words associated with that quote that will be changed by the user
                for index, word in enumerate(quote['words']):

                    if not Word.query.filter_by(text=quote['text'], position=index, quote_id=new_quote.id).first():
                        new_word = Word(text=word, position=index, quote_id=new_quote.id)
                        db.session.add(new_word)
                        db.session.commit()
                    
                print('Tweetry Manager: A new quote was added.')

        return

    #Places a vote for the specified choice, voting multiple times will cause the 
    #user's prior vote to be removed each time
    def save_vote(self, choice, ip_address):

        current_tweetry = self.get_current_tweetry()

        #Here we are checking to see if the user is voting for the current tweetry
        #if it is an old one we send a refresh message back to the client to reload the page
        if int(choice['tweetryId']) != current_tweetry.id:
            return 'Refresh'

        word_id = db.session.query(Word).filter_by(text=choice['word'], position=choice['position'], quote_id=current_tweetry.quote_id).first().id

        #If the choice is the default word we do nothing and leave
        if db.session.query(Word).filter_by(text=choice['choice'], id=word_id).first():
            return 'Failed'

        existing_choice = db.session.query(Choice).filter_by(text=choice['choice'], word_id=word_id, tweetry_id=current_tweetry.id).first()
        
        #If the choice already existed
        if not existing_choice: #Create it 
            new_choice = Choice(text=choice['choice'], word_id=word_id, votes=1, tweetry_id=current_tweetry.id)
            db.session.add(new_choice)
            db.session.commit()
            choice_id = new_choice.id
            print('Tweetry Manager: A new choice was added: "{}"'.format(choice['choice']))
        else:
            existing_choice.votes += 1
            db.session.commit()
            choice_id = existing_choice.id
            print('Tweetry Manager: Choice Exists! Vote count for "{}" is now {}'.format(choice['choice'], existing_choice.votes))

        self.update_last_choice(ip_address, choice_id)

        return 'Success'

    #Updates the user's last choice and checks to see if we need to decrement the vote count
    #or if the user is voting for the first time we add them to the ip list
    def update_last_choice(self, ip_address, choice_id):

        found = False   

        for ip in self.voted_ips:
            if(ip['ip'] == ip_address):
                found = True
                #Decrement last choice vote
                last_choice = db.session.query(Choice).filter_by(id=ip['last_choice_id']).first()
                last_choice.votes -= 1

                if(last_choice.votes == 0):
                    db.session.query(Choice).filter_by(id=ip['last_choice_id']).delete()

                db.session.commit()
                ip['last_choice_id'] = choice_id

        #Otherwise we add them to the list
        if found == False:
            self.voted_ips.append({ 
                'ip' : ip_address,
                'last_choice_id' : choice_id
            })

        return

    #Gets the top choice for specified word
    def get_top_choice(self, word_data):

        word_id = db.session.query(Word).filter_by(text=word_data['word'], position=word_data['position']).first().id
        choice = db.session.query(Choice).filter_by(word_id=word_id, tweetry_id=word_data['tweetryId']).order_by(db.desc('votes')).first()

        if choice:
            top_choice = {
                'word' : choice.text,
                'votes' : choice.votes
            }

            return top_choice
        else:
            return 'Failed'

    #Gets the top choices for the specified word and returns a dictionary of those choices
    def get_top_choices(self, word_data):

        word_id = db.session.query(Word).filter_by(text=word_data['word'], position=word_data['position'], quote_id=word_data['quoteId']).first().id
        choices = db.session.query(Choice).filter_by(word_id=word_id, tweetry_id=word_data['tweetryId']).order_by(db.desc('votes')).limit(10).all()

        top_choices = {}
        
        for choice in choices:
            top_choices[choice.text] = { 
                'word'  : choice.text,
                'votes' : choice.votes
            }

        return top_choices

    #Returns the current tweetry object
    def get_current_tweetry(self):
        return db.session.query(Tweetry).filter_by(id=self.current_tweetry_id).first()
