
from application.quotes import quotes
from application.models import Quote, Word, Tweetry, Choice
from application import db
import random, re

class TweetryManager:

    def __init__(self):
        print('Tweetry Manager: Initialized')
        self.check_for_new_quotes()
        self.current_tweetry_id = self.create_new_tweetry()

    #Create new tweetry and add to database
    def create_new_tweetry(self):
        tweetry = Tweetry(quote_id=random.randint(1, db.session.query(Quote).count()))
        db.session.add(tweetry)
        db.session.commit()
        #return tweetry
        return tweetry.id

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

    #TO DO: Need to prevent users from voting more than once
    def update_choices(self, choices):

        tweetry = self.get_current_tweetry()

        for index, choice in enumerate(choices):

            word_id = tweetry.quote.words[index].id

            #If the choice is the default word, next iteration
            if db.session.query(Word).filter_by(text=choice, id=word_id).first():
                continue

            existing_choice = db.session.query(Choice).filter_by(text=choice, word_id=word_id, tweetry_id=self.current_tweetry_id).first()
            #If we do not have a choice created yet for the word that we are enumerating
            if not existing_choice: #Create it
                new_choice = Choice(text=choice, word_id=word_id, votes=1, tweetry_id=self.current_tweetry_id)
                db.session.add(new_choice)
                db.session.commit()
                print('Tweetry Manager: A new choice was added: "{}"'.format(choice))
            else:                   #or increase the vote count
                existing_choice.votes += 1
                db.session.commit()
                print('Tweetry Manager: Choice Exists! Vote count for "{}" is now {}'.format(choice, existing_choice.votes))

        return

    #Gets the top choices for the specified word and returns a dictionary of those choices
    def get_top_choices(self, word_data):
        
        word_id = db.session.query(Word).filter_by(text=word_data['word'], position=word_data['position']).first().id
        choices = db.session.query(Choice).filter_by(word_id=word_id, tweetry_id=self.current_tweetry_id).order_by(db.desc('votes')).all()

        top_choices = {}
        
        for choice in choices:
            top_choices[choice.text] = { 
                'word'  : choice.text,
                'votes' : choice.votes
                }

        return top_choices

    #Gets the top choice for specified word
    def get_top_choice(self, word_data):

        word_id = db.session.query(Word).filter_by(text=word_data['word'], position=word_data['position']).first().id
        choice = db.session.query(Choice).filter_by(word_id=word_id, tweetry_id=self.current_tweetry_id).order_by(db.desc('votes')).first()

        if choice:
            top_choice = {
                'word' : choice.text,
                'votes' : choice.votes
            }

            return top_choice
        else:
            return 'Failed'

    #Returns the current tweetry object
    def get_current_tweetry(self):
        return db.session.query(Tweetry).filter_by(id=self.current_tweetry_id).first()
