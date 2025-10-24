from flask import Blueprint
from src.services.implementation.ProfileService import ProfileService

profileController = Blueprint("profileController", __name__, url_prefix="/profile")
profileService = ProfileService()

@profileController.route('edit', methods=["POST"])
def edit_profile(data):
    profileService.edit_profile(data)

@profileController.route("me")
def me():
    pass