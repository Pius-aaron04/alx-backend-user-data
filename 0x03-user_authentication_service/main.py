#!/usr/bin/env python3
"""
Task 20 Main file
"""

import requests
BASE_URL = "http://0.0.0.0:5000/"
EMAIL = "guillaume@holberton.io"
PASSWD = "b410u"
NEW_PASSWD = "t4trt1f13tt3"


def register_user(email: str, password: str) -> None:
    """Sends request to register user."""

    url = BASE_URL + 'users'

    res = requests.post(url, data={"email": email, "password": password})

    assert 200 == res.status_code
    assert {"email": email, "message": "user created"} == res.json()


def log_in_wrong_password(email: str, password: str) -> None:
    """Tests User auth service with wrong password.
    """

    url = BASE_URL + 'sessions'

    res = requests.post(url, data={"email": email, "password": password})

    assert 401 == res.status_code


def log_in(email: str, password: str) -> str:
    """Tests User auth service with correct password.
    """

    url = BASE_URL + 'sessions'
    res = requests.post(url, data={"email": email, "password": password})

    assert 200 == res.status_code
    assert {"email": email, "message": "logged in"} == res.json()
    session_id = res.cookies.get('session_id')
    return session_id


def profile_unlogged() -> None:
    """retreiving user profile while not logged in
    """

    url = BASE_URL + 'profile'
    res = requests.get(url)
    assert 403 == res.status_code


def profile_logged(session_id: str) -> None:
    """Tests profile endpoint with session_id.
    """
    url = BASE_URL + 'profile'
    res = requests.get(url, cookies={'session_id': session_id})

    assert 200 == res.status_code
    assert {"email": EMAIL} == res.json()


def log_out(session_id: str) -> None:
    """Tests user logout
    """

    url = BASE_URL + 'sessions'
    res = requests.delete(url, cookies={'session_id': session_id})
    assert 200 == res.status_code


def reset_password_token(email: str) -> str:
    """gets reset password token."""
    url = BASE_URL + 'reset_password'
    res = requests.post(url, data={"email": email})
    assert 200 == res.status_code
    assert 'reset_token' in res.json()
    return res.json()['reset_token']


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """Updates user password"""

    url = BASE_URL + 'reset_password'
    res = requests.put(url, data={"email": email, "reset_token": reset_token,
                                  "new_password": new_password})
    assert 200 == res.status_code
    assert {"email": email, "message": "Password updated"} == res.json()


if __name__ == '__main__':
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    session_id = log_in(EMAIL, PASSWD)
    profile_unlogged()
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
