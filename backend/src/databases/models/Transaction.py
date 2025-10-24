from src import db

class Transaction(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    amount= db.Column(db.Float(), nullable=False)
    user_id= db.Column(db.Integer())
