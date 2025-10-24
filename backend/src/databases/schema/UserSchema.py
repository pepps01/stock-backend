# from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from src.databases.models.User import User
# from src import marshmallow

class UserSchema():
    class Meta:
        model = User
        load_instance = True
        exclude = ("password",)
