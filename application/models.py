
from application import db

class Quote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(), nullable=False)
    text = db.Column(db.String(), unique=True, nullable=False)

    def __repr__(self):
        return f"Quote('{ self.author }, { self.text }')"