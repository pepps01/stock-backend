from abc import ABCMeta, ABC, abstractmethod

class UserInterface(metaclass=ABCMeta):

    @abstractmethod
    def register(self, userData: dict):
        pass

    @abstractmethod
    def forgot_password(self, userData: dict):
        pass

    @abstractmethod    
    def me(self):
        pass

    @abstractmethod    
    def get_users(self):
        pass

    @abstractmethod
    def deactivate_users(self):
        pass
    
    @abstractmethod
    def get_user_by_email(self, email: str):
        pass