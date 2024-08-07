#!/usr/bin/env python3

"""Session Authentication class definition for session management
"""
from .auth import Auth
from os import getenv
from uuid import uuid4
from models.user import User


class SessionAuth(Auth):
    """Session Auth for User session management.
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """Creates a session ID for user with user_id
        Return:
          - Session ID with uuid4 value as its value
          - None if user_id is None or is not a str
        """

        if not isinstance(user_id, str) or not user_id:
            return None

        session_id = str(uuid4())

        SessionAuth.user_id_by_session_id[session_id] = user_id

        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """Gets user_id for session_id
        Return
          - corresponding user_id
          - None if session_id is None or not a string
          - None if session_id is not found 
        """

        if not isinstance(session_id, str) or not session_id:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """Gets current user object
        Return
         - User object based on session
         - return None if request is None or if user couldn't be fetched
        """

        session = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session)

        if not user_id:
            return None
        return User.get(user_id)
