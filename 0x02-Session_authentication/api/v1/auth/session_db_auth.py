#!/usr/bin/env python3
"""DB based Session management system.
"""
from .session_exp_auth import SessionExpAuth
from models.user_session import UserSession


class SessionDBAuth(SessionExpAuth):
    """Persistent session management.
    """

    def create_session(self, user_id=None):
        """creates session for user
        """
        if user_id is None or not isinstance(user_id, str):
            return None
        session_id = super().create_session(user_id)

        user_session = UserSession(user_id=user_id, session_id=session_id)
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """Fetches user_id for specified session"""

        if session_id is None and not isinstance(session_id, str):
            return None

        try:
            user_id = UserSession.search({'session_id': session_id})[0].user_id

            if user_id is None:
                return None
        except KeyError:
            return None
        return user_id
