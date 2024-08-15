#!/usr/bin/env python3
"""Simple Flask App"""

from auth import Auth
from flask import Flask, jsonify, request, abort, redirect
from flask import make_response

app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"])
def index():
    return jsonify({"message": "Bievenue"}), 200


@app.route("/users", methods=["POST"])
def register_user():
    """Registers user
    Request payload:
      - email
      - password
    Return:
      - 200 on success with email and message as response payload
      - 400 if user already exists
    """

    payload = request.form
    email = payload.get("email")
    password = payload.get("password")

    if all((email, password)):
        try:
            user = AUTH.register_user(email, password)
        except ValueError:
            return jsonify({"message": "email already registered"}), 400
        return jsonify({"email": user.email, "message": "user created"}), 200


@app.route("/sessions", methods=["POST"])
def login():
    """Logs in user"""

    password = request.form.get('password')
    email = request.form.get('email')

    if not AUTH.valid_login(email, password):
        abort(401)

    response = make_response(jsonify({"email": email, "message": "logged in"}))
    session_id = AUTH.create_session(email)
    response.set_cookie('session_id', session_id)

    return response, 200


@app.route("/sessions", methods=["DELETE"])
def logout():
    """Logs user out."""

    session_id = request.cookies.get('session_id')
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"])
def user_profile():
    """gets current user data"""

    session_id = request.cookies.get('session_id')
    if not session_id:
        abort(403)
    user = AUTH.get_user_from_session_id(session_id)

    if not user:
        abort(403)
    return jsonify({"email": user.email}), 200


@app.route("/reset_password", methods=["PUT"])
def reset_passwd():
    """Updates user pwd
    Payload:
      - email
      - reset_token
      - new_password
    Return:
      - 200 on success
      - 403 if credentials are invalid
    Response:
      {"email" : "<user email>", "message" : "password updated"}
    """
    try:
        email = request.form.get('email')
        reset_token = request.form.get('reset_token')
        new_password = request.form.get('new_password')

        AUTH.update_password(reset_token, new_password)
    except ValueError:
        abort(403)

    return jsonify({"email": email, "message": "Password updated"}), 200


@app.route("/reset_password", methods=["POST"])
def get_reset_token():
    """Generates a reset password token for user.
    payload:
      - email
    Return:
      - 200 on success
      - 403 if email is not registered
    """

    email = request.form.get('email')
    try:
        reset_token = AUTH.get_reset_password_token(email)
    except ValueError:
        abort(403)
    return jsonify({"email": email, "reset_token": reset_token}), 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
