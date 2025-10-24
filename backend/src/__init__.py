from flask import Flask, request, jsonify
import pika
from flask_cors import CORS

# from flask_socketio import SocketIO
# import pytest
from dotenv import load_dotenv
from flask_jwt_extended import (JWTManager)
from datetime import timedelta
import redis
# from flask_restful import Resource, fields, marshal_with
# # from config import Config
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase
import logging
from flask_socketio import SocketIO, emit
from flask_bcrypt import Bcrypt
# from flask_marshmallow import Marshmallow


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
# print(socketio.emit("response", {"data": f'Server recieved:'}, broadcast=True))

# JWT configuration
app.config["JWT_SECRET_KEY"] = "super-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
app.config["JWT_BLACKLIST_ENABLED"] = True

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:rootpassword@mysql_db:3306/flask_db"
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://flask_user:flask_pass@mysql_db:3306/flask_db"

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
jwt = JWTManager(app)
cors = CORS(app=app)
bcrypt = Bcrypt(app)
# marshmallow = Marshmallow(app)

class Base(DeclarativeBase):
  pass

db = SQLAlchemy(model_class=Base)
db.init_app(app)
migrate = Migrate(app=app, db=db)


# from src.databases.models.User import User
# from src.databases.models.Profile import Profile
# from src.databases.models.Transaction import Transaction


# from src.controllers.AuthController import authController
# from src.controllers.UserController import userController
# from src.controllers.ProfileController import profileController
# from src.controllers.SelectorController import selectorController


# migrate = Migrate(app)
# # CORS(app, origins=["http://localhost:3000", "https://myfrontend.com/"])
app.config["JWT_SECRET_KEY"] = "super-secret-key"  # change this!
# app.register_blueprint(authController)
# app.register_blueprint(userController)
# app.register_blueprint(profileController)
# app.register_blueprint(selectorController)


# API_KEY = "my_secret_api_key"

blacklist = set()
@jwt.token_in_blocklist_loader
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

@app.route('/protected')
def protected():
    logging.info("olk")
    return jsonify({"message": "Welcome to the protected route!"})

# bluepant
@app.route("/")
def hello():
    socketio.emit('response', {'data': 'Got it!'})
    # print("Grace", socketio.emit('response', {'data': 'Got it!'}))
    
    db.create_all()
    return "Hello from Flask + Requested use for this Werldfg!"

@app.route("/let")
def relay():
    print(load_dotenv())
    return "Rest!"

@app.route("/heatlh")
def healthcheck():
    return "Server is running!"

def get_rabbitmq_connection():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="rabbitmq")
    )
    return connection

@app.route("/publish", methods=["POST"])
def publish_message():
    data = request.json()
    message = data.get("message", "Hello RabbitMQ")

    connection = get_rabbitmq_connection()
    channel = connection.channel()
    channel.queue_declare(queue="test_queue", durable=True)

    channel.basic_publish(exchange="",
                          routing_key="test_queue",
                          body=message)

    connection.close()
    return

@app.route("/test-ing")
def create_test():
    # from src.repositories.UserRepository import UserRepository
    # data =  request.get_json()
    data = {"firstname": "Sunny", }
    # UserRepository.create_user(data)
    return jsonify({ "data": "User Created" })

# @app.route("/test", methods=["POST"])
# def render():
#     # from src.models.User import User
#     # data = {
#     #     "firstname":"Sunny",
#     #     "lastname":"Pepple",
#     #     "email": "slpepple01@gmail.com",
#     #     "password":"password"
#     # }

#     data = request.get_json()

#     firstname = data.get("firstname")
#     lastname = data.get("lastname")
#     email = data.get("email")
#     password = data.get("password") 

#     if not all([firstname, lastname, email, password]):
#         return jsonify({"error": "Missing required fields"}), 400

#     hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

#     new_user = User(
#         firstname=firstname,
#         lastname=lastname,
#         email=email,
#         password=hashed_password
#     )

#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({
#         "message": "User created successfully",
#         "user": {
#             "firstname": firstname,
#             "lastname": lastname,
#             "email": email
#         }
#     }), 201

    # if request.method ==  "POST":
    #     firstname = request.get_json()["firstname"]
    #     print("firstname",firstname)
    #     # firstname = firstname["firstname"]
    #     return jsonify({
    #         "firstname": firstname,
    #         "details":"Sent"
    #     })

    
# === Create tables ===
with app.app_context():
    # from src.models.User import User
    # from src.models.Profile import Profile
    # from src.models.Transaction import Transaction
    db.create_all()


