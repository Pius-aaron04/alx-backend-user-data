#!/usr/bin/env python3
"""Password hashing."""

from bcrypt import hashpw, gensalt, checkpw
from db import DB
from sqlalchemy.exc import NoResultFound


def _hash_password(password: str) -> str:
    """Returs a hashed password in bytes."""

    password = password.encode('utf-8')
    return hashpw(password, gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email, password):
        """Registers user to db"""

        try:
            user = self._db.find_user_by(email=email)
            raise ValueError('{} already exists'.format(email))
        except NoResultFound:
            password=_hash_password(password).decode('utf-8')
            user = self._db.add_user(email=email, hashed_password=password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        pwd_hash = user.hashed_password.encode('utf-8')
        return checkpw(password.encode('utf-8'), pwd_hash)
