
from application import db

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), unique=True, nullable=False)
    words = db.relationship('Word', backref='quote', lazy=True)

    def __repr__(self):
        return f"Quote('{ self.author }, { self.text }')"

class Word(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(), nullable=False)
    position = db.Column(db.Integer, nullable=False)
    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'), nullable=False)

    def __repr__(self):
        return f"Word('{ self.text }, { self.position }, { self.quote_id }')"