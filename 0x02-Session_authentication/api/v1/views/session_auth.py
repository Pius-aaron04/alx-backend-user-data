#!/usr/bin/env python3
"""Session Authentication management endpoints.
"""
from api.v1.views import app_views
from flask import request, make_response, jsonify
from models.user import User
from os import getenv


@app_views.route('/auth_session/login', strict_slashes=False,
                 methods=['POST'])
def session_login():
    """Logs in user
    Return
      - User Object with 200 status
      - error 400
        - if email is missing
        - if password field is missing
    """

    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    elif not password:
        return jsonify({"error": "password missing"}), 400

    try:
        users = User.search({"email": email})
        if len(users) == 0:
            return jsonify({"error": "no user found for this email"}), 404
    except KeyError:
        return jsonify({"error": "no user found for this email"}), 404

    for user in users:
        if user.is_valid_password(password):
            from api.v1.app import auth
            session = auth.create_session(user.id)
            response = make_response(user.to_json(), 200)
            response.set_cookie(getenv('SESSION_NAME'), session)
            return response
    return jsonify({"error": "wrong password"}), 401


@app_views.route('/auth_session/logout', strict_slashes=False,
                 methods=['DELETE'])
def session_logout():
    """Logs out the current user.
    Return
      - 200 with empty data
      - 404 if no session ID is found or session id is invalid
    """
    from api.v1.app import auth
    if auth.destroy_session(request):
        return jsonify({}), 200
    abort(404)
