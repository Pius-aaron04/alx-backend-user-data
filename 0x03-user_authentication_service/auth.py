#!/usr/bin/env python3
"""Password hashing."""

import bcrypt
from db import DB
from sqlalchemy.orm.exc import NoResultFound
from typing import Union, TypeVar
import uuid


def _hash_password(password: str) -> bytes:
    """hashes a password in string.
    Returns:
      - bytes
    """

    password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password, salt)


def _generate_uuid() -> str:
    """generates a uuiq"""

    return str(uuid.uuid4())


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
            password = _hash_password(password).decode('utf-8')
            user = self._db.add_user(email=email, hashed_password=password)

        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validates user login"""

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            return False

        pwd_hash = user.hashed_password.encode('utf-8')
        return bcrypt.checkpw(password.encode('utf-8'), pwd_hash)

    def create_session(self, email: str) -> str:
        """Creates a session for email
        Return
          - session id
        """

        try:
            user = self._db.find_user_by(email=email)
            session_id = str(_generate_uuid())
            self._db.update_user(user.id, session_id=session_id)
        except NoResultFound:
            return None

        return session_id

    def get_user_from_session_id(self, session_id: str)\
            -> Union[TypeVar('User'), None]:
        """get user from session.
        Return:
          - User instance
          - None if user not found or session id is invalid
        """

        if not session_id:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """destroys user session"""

        self._db.update_user(user_id, session_id=None)

    def get_reset_password_token(self, email: str) -> str:
        """Generates reset token for user.
        """

        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError

        reset_token = _generate_uuid()

        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """updates user password."""

        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError

        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        self._db.update_user(user.id,
                             hashed_password=hashed_pwd.decode('utf-8'),
                             reset_token=None)
