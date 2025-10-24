from src.databases.models.Profile import Profile

class ProfileRepository(Profile):
    def __init__(self):
        pass

    def create_profile(self,data):
        profile = Profile()