from flask_jwt_extended import create_access_token
# from flask_jwt_extended import get_jwt_identity
# from flask_jwt_extended import jwt_required
# from flask_jwt_extended import JWTManager
# from src.repositories.UserRepository import UserRepository
import logging
from src.repositories.UserRepository import UserRepository

class AuthService:
    def __init__(self):
        self.repository = UserRepository()
        pass

    def login(self, data):
        logging.info("Rendered issues")
        # check if its in the database 
        # cretaed a create_access_token
        if self.repository.check_user(data['email']):
            return False
        return create_access_token(data['email'])
           
    def logout(self):
        logging.info("Rendered issues")


    def check_with_me(self):
        pass