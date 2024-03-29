from flask import request, make_response, jsonify
from functools import wraps
from mongoengine import DoesNotExist, ValidationError
from werkzeug.security import generate_password_hash, check_password_hash
import jwt

from app import app
from data import User

# TODO: This module is temproary, all authentication will be handled through flask-login in future.

def auth_required(f):
    @wraps(f)
    def decorater(*args, **kwargs):
        # TODO: CHECK AUTH HEADER EXITS

        auth_type, access_token = request.headers.get("Authorization").split(" ")

        if auth_type != "Bearer" or auth_type is None:
            return make_response(
                jsonify({"message": "Invalid authorization token."}), 401
            )

        try:
            data = jwt.decode(
                access_token, app.config["SECRET_KEY"], algorithms=["HS256"]
            )
            current_user = User.objects.get(name__exact=data["user_name"])
        except:
            return make_response(
                jsonify({"message": "Invalid authorization token."}), 401
            )

        return f(current_user=current_user, *args, **kwargs)

    return decorater


@app.route("/login", methods=["POST"])
def login():
    auth = request.get_json()
    if not auth or not auth.get("username") or not auth.get("password"):
        return make_response(jsonify({"message": "Invalid login credentials."}), 401)

    try:
        user = User.objects.get(name=auth["username"])
    except DoesNotExist:
        return make_response(jsonify({"message": "User does not exits"}), 401)

    if check_password_hash(user.pass_hash, auth.get("password")):
        token = jwt.encode({"user_name": user.name}, app.config["SECRET_KEY"], "HS256")
        return make_response(jsonify({"token": token}), 201)

    return make_response(jsonify({"message": "Invalid username or password."}), 401)


@app.route("/register", methods=["POST"])
def register():
    new_user_json = request.get_json()
    if not new_user_json:
        return make_response(
            jsonify({"message": "user name and password required."}), 400
        )

    existing_user = User.objects(name=new_user_json["username"])
    if not existing_user:
        new_user = User(
            name=new_user_json.get("username"),
            pass_hash=generate_password_hash(
                new_user_json.get("password"), method="sha256"
            ),
        )

        try:
            new_user.validate()
            new_user.save()
        except ValidationError:
            return make_response(
                jsonify({"message": "Invalid user name or password."}), 400
            )

        return make_response(jsonify({"message": "User created."}), 200)

    return make_response(jsonify({"message": "username already exits."}), 400)
