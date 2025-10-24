from flask import Blueprint, jsonify, request
from flask_jwt_extended import (
     create_access_token, jwt_required, get_jwt_identity, get_jwt,create_refresh_token
)
import redis
import time
from datetime import timedelta
from src.services.implementation.AuthService import AuthService
# from src.services.implementation.UserService import UserService
authService= AuthService()

# from src.services.implementation.AuthService import AuthService
authController = Blueprint('authController', __name__)

@authController.route('/login', methods=["POST"])
def login():
    return 1
    firstname = request.json.get("firstname")
    password = request.json.get("password")
    # if firstname not in users or users[username] != password:
    #     return jsonify({"msg": "Bad username or password"}), 401
    # CHECK THE USER IS NOT IN THE DB
    access_token = create_access_token(identity=firstname)
    refresh_token = create_refresh_token(identity=firstname)

    return jsonify({"access_token":access_token,})


blacklist = set()
def check_if_token_revoked(jwt_header, jwt_payload):
    jti = jwt_payload["jti"]
    return jti in blacklist

@authController.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged_in_as=current_user), 200


# --- LOGOUT ROUTE ---
@authController.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    jti = get_jwt()["jti"]  # unique token ID
    exp_timestamp = get_jwt().get("exp", 0)

    now = int(time.time())
    ttl = int(exp_timestamp) - now
    if ttl <= 0:
        ttl = 1
    # Store jti in redis with TTL
    # redis_client.setex(jti, ttl, "revoked")
    return jsonify(msg="Access token revoked"), 200

    # blacklist.add(jti)
    return jsonify(msg="Successfully logged out"), 200


# --- Refresh endpoint (issue new access token using refresh token) ---
@authController.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    new_access = create_access_token(identity=identity)
    return jsonify(access_token=new_access), 200