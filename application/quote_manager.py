
from application.quotes import quotes
from application.models import Quote, Word
from application import db
import random

class QuoteManager:

    def __init__(self):
        print('Quote Manager: Initialized')
        self.check_for_new_quotes()
        self.current_quote = self.get_random_quote()

    def get_random_quote(self):
        return quotes[random.randint(0, len(quotes)-1)]

        
    def check_for_new_quotes(self):

        #Iterating over list of quotes in quotes.py
        for quote in quotes:

            #If we have come across a quote that did not exist we insert it
            if not Quote.query.filter_by(text=quote['text']).first():
                
                new_quote = Quote(author=quote['author'], text=quote['text'])
                db.session.add(new_quote)
                db.session.commit()
                
                #We also insert the words associated with that quote that will be changed
                for index, word in enumerate(quote['words']):

                    if not Word.query.filter_by(text=quote['text'], position=index, quote_id=new_quote.id).first():
                        new_word = Word(text=word, position=index, quote_id=new_quote.id)
                        db.session.add(new_word)
                        db.session.commit()
                    
                print('Quote Manager: A new quote was added.')

        return
