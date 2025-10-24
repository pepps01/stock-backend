# share the errors 
# controll the naratives
from flask import Blueprint, request, jsonify
from src.services.implementation.UserService import UserService
from src.services.interface.UserInterface import UserInterface


userController = Blueprint('userController',__name__, url_prefix="/api")
# from src import socketio, emit
userService = UserService()


@userController.route("/register", methods=["POST"])
def register():
   data = request.get_json()
   if not data:
      return jsonify({"error": "Invalid request"}), 400
   
   existing_user = userService.get_user_by_email(data.get("email"))
   if existing_user:
      return jsonify({"error": "User already exists"}), 400   
  
   user = userService.register(data)
   return jsonify({
      "message": "User created successfully",
      "user" : {
         "email": user.email,
         "firstname": user.firstname,
         "lastname": user.lastname
      }
   }),201


@userController.route("/me", methods=["POST"])
def me():
   return

@userController.route("/users")
def get_users():
   pass

@userController.route("/deactivate", methods=["POST"])
def deactivate_users():
   return

@userController.route("/forgot-password", methods=["POST"])
def forgot_password():
   return

# @userController.route("/message", methods=["GET"])
# @socketio.on("custom_event")
# def handle_message(data):
#    print("Custom Event, data")
#    emit("response", {"data": f'Server recieved: {data}'}, broadcast=True)
   