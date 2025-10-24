from marshmallow import Schema, fields
from src import db
# tie the schema to the  user repo
from src.databases.models.User import User
from src.databases.schema.UserSchema import UserSchema

class UserRepository:
    def __init__(self):
        pass

    @classmethod
    def create_user( userData):
        new_user = User(
            firstname=userData["firstname"],
            lastname=userData["lastname"],
            email=userData["email"],
            password=userData['password']
        )
        return new_user
    
    def get_user(self):
        return User.query.all()

    def get_user_by_roles(self):
        users = db.session.execute(db.select(User).order_by(User.role)).scalars()
        return users
    
    def get_single_user(self, email):
        user = db.session.execute(db.select(User).filter_by(email)).scalar_one()
        return user

    def update_user(self, data):
        user = User()
        if data["firstname"] is None:
            # maybe an exception here it is very important to add what needs to be 
            # here 
            return  
        if data["lastname"] is None:
            return False
        
        user.firstname = data["firstname"]
        user.lastname= data["lastname"]
        db.session.commit()

        
    def delete_user(self, email):
        user =  User.query.filter_by(email=email).first()
        db.session.delete(user.id)
        db.session.commit()
        return "user deleted"

    def check_user(self, email):
        return True