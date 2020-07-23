
from application.quotes import quotes
from application.models import Quote, Word, Tweetry, Choice
from application import db
import random, re, json, datetime, tweepy, keys

class TweetryManager:

    #Checks our quotes.py file to see if any new quotes have been added    
    def check_for_new_quotes(self):

        #Iterating over list of quotes in quotes.py
        for quote in quotes:
            
            #If we have come across a quote that did not exist we insert it
            if not Quote.query.filter_by(text=quote['text']).first():

                new_quote = Quote(author=quote['author'], fake_author=self.create_fake_author_name(quote['author']), text=quote['text'])
                db.session.add(new_quote)
                db.session.commit()

                #Splitting our quote into separate words (no whitespace or punctuation)
                word_list = re.split('([\s.,;()]+)', quote['text'])
                formatted_text= ''

                position = 0

                for word in word_list:

                    #If it is a legit word (starts with a letter) we add it 
                    if word and word[0].isalpha():

                        new_word = Word(text=word, position=position, quote_id=new_quote.id)
                        db.session.add(new_word)
                        db.session.commit()

                        #Our formatted text will be what is displayed on the page
                        formatted_text += f'<span class="quote-word" data-position="{ position }" data-word="{ word }" data-word-id="{ new_word.id }">{ word }</span>'

                        position += 1
                    else:
                        formatted_text += word

                new_quote.formatted_text = formatted_text
                db.session.commit()

                print('Tweetry Manager: A new quote was added.')

        return

    #Create new tweetry and add to database
    def create_new_tweetry(self):

        old_tweetry = db.session.query(Tweetry).filter_by(is_active=True).first()

        if old_tweetry:
            old_tweetry.is_active = False
            db.session.commit()

        new_tweetry = Tweetry(quote_id=random.randint(1, db.session.query(Quote).count()))
        db.session.add(new_tweetry)
        db.session.commit()
        return

    #This will reverse the first and last letters of the first and last word of a string to create 
    #a 'fake' author name for quotes that have been edited
    def create_fake_author_name(self, author_name):

        split_name = author_name.split(' ')

        first_name_letter = split_name[0][0]
        last_name_letter = split_name[-1][0]
        
        fake_first_name = last_name_letter + split_name[0][1:]
        fake_last_name = first_name_letter + split_name[-1][1:]

        #If the name is larger than two words we need to get all the stuff inbetween and add it back in
        if(len(split_name) > 2):
            fake_full_name = fake_first_name + ' ' + ' '.join(split_name[1:-1]) + ' ' + fake_last_name
        else:
            fake_full_name = fake_first_name + ' ' + fake_last_name

        return fake_full_name

    #Constructs our final quote and returns it in a string
    def create_final_quote(self):

        tweetry = self.get_current_tweetry()
        original_quote = tweetry.quote

        word_list = re.split('([\s.,;()]+)', original_quote.text)

        final_quote = ''

        position = 0

        for word in word_list:

            if word and word[0].isalpha():

                word_id = db.session.query(Word).filter_by(position=position, quote_id=tweetry.quote.id).first().id
                top_choice = db.session.query(Choice).filter_by(tweetry_id=tweetry.id, word_id=word_id).first()
                
                if top_choice:
                    final_quote += top_choice.text
                else:
                    final_quote += word

                position += 1

            else:
                final_quote += word

        if(final_quote == original_quote.text):
            final_quote = f'\"{final_quote}\" -{original_quote.author}'
        else:
            final_quote = f'\"{final_quote}\" -{original_quote.fake_author}'

        return final_quote

    #Places a vote for the specified choice, voting multiple times will cause the 
    #user's prior vote to be removed each time
    def save_vote(self, choice):

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

        #If we passed in a last choice value we need to decrement the user's last vote
        if choice['lastChoice']:
            self.update_last_choice(choice['lastChoice'], current_tweetry.id)

        return str(choice_id)

    #Updates the user's last choice and checks to see if we need to decrement the vote count
    def update_last_choice(self, choice_id, tweetry_id):

        last_choice = db.session.query(Choice).filter_by(id=choice_id, tweetry_id=tweetry_id).first()

        if last_choice:
            last_choice.votes -= 1

            if(last_choice.votes == 0):
                db.session.query(Choice).filter_by(id=choice_id).delete()

            db.session.commit()

        return

    #Gets the top choice for specified word
    def get_top_choice(self, word_data):

        choice = db.session.query(Choice).filter_by(word_id=word_data['wordId'], tweetry_id=word_data['tweetryId']).order_by(db.desc('votes')).first()

        if choice:
            top_choice = {
                'word' : choice.text,
                'votes' : choice.votes
            }

            return top_choice
        else:
            return 'Failed'

    #Returns a list of the top choice for each of the specified words
    def get_top_choice_for_words(self, words_data):

        top_choice_list = []

        for word in words_data:

            top_choice = db.session.query(Choice).filter_by(word_id=word['wordId'], tweetry_id=word['tweetryId']).order_by(db.desc('votes')).first()

            if top_choice:
                top_choice_list.append( {
                    'topChoice' : top_choice.text,
                    'wordId' : top_choice.word_id,
                    'votes' : top_choice.votes
                })  

        return top_choice_list

    #Gets the top choices for the specified word and returns a dictionary of those choices
    def get_top_choice_list(self, word_data):

        choices = db.session.query(Choice).filter_by(word_id=word_data['wordId'], tweetry_id=word_data['tweetryId']).order_by(db.desc('votes')).limit(10).all()

        top_choices = {}
        
        for choice in choices:
            top_choices[choice.text] = { 
                'word'  : choice.text,     
                'votes' : choice.votes
            }

        return top_choices

    #Returns the current tweetry object from the database
    def get_current_tweetry(self):
        return db.session.query(Tweetry).filter_by(is_active=True).first()

    #Tweets our newly created quote
    def tweet_final_quote(self):

        final_quote = self.create_final_quote()

        try:
            auth = tweepy.OAuthHandler(keys.api_key, keys.api_secret_key)
            auth.set_access_token(keys.access_token, keys.access_token_secret)

            api = tweepy.API(auth)

            api.update_status(f'{final_quote} - {datetime.datetime.now().date()}')
        except:
            print('Tweet failed to post.')

        return final_quote
