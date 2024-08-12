#!/usr/bin/env python3
"""Simple Flask App"""

from auth import Auth
from flask import Flask, jsonify, request

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


if __name__ == '__main__':
    app.run(host="0.0.0.0", port="5000")
