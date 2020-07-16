
from application import db

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), unique=True, nullable=False)
    words = db.relationship('Word', backref='quote', lazy=True)
    tweetry = db.relationship('Tweetry', backref='quote', lazy=True)

    def __repr__(self):
        return f"Quote('{ self.author }, { self.text }')"

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)  
    choices = db.relationship('Choice', backref='word', lazy=True) 

    def __repr__(self):
        return f"Word('{ self.text }, { self.position }, { self.quote_id }')"

class Tweetry(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)
    choices = db.relationship('Choice', backref='tweetry', lazy=True)

    def __repr__(self):
        return f"Tweetry('quote:{ self.quote.text }, choices:{ self.choices }')"

class Choice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(20), nullable=False)
    votes = db.Column(db.Integer, default=0, nullable=False)
    word_id = db.Column(db.Integer, db.ForeignKey('word.id'), nullable=False)
    tweetry_id = db.Column(db.Integer, db.ForeignKey('tweetry.id'), nullable=False)

    def __repr__(self):
        return f"Choice('text:{ self.text }, votes:{ self.votes }, word_id: { self.word_id }, tweetry_id:{ self.tweetry_id }')"

