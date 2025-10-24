from src import db

class Profile(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    password= db.Column(db.String(50))
    user_id= db.Column(db.Integer())    
    user = db.relationship("User", backref=db.backref("profiles", lazy=True))
    
