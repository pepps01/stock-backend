from src import db
from marshmallow import Schema, fields

#  TODO:What is marshmallow for 
class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    firstname= db.Column(db.String(50))
    lastname= db.Column(db.String(50))
    email= db.Column(db.String(100), nullable=False)
    password= db.Column(db.String(250), nullable=False)
