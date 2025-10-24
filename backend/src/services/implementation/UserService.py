from src.repositories.UserRepository import UserRepository
from src.services.interface.UserInterface import UserInterface
from src import bcrypt
from src.services.external.Mail  import Mail

user_repository = UserRepository()
mail = Mail()

class UserService(UserInterface):

    def register(self, userData):
        userData["password"] =  bcrypt.generate_password_hash(data["password"]).decode("utf-8")
        new_user = user_repository.create_user(userData)
        mail.send()
        return new_user
    
    def forgot_password(self, userData):
        return
    
    def me(self):
        return
    
    def get_users(self):
        pass

    def deactivate_users(self):
        return
    
    def get_user_by_email(self, email: str):
        return
