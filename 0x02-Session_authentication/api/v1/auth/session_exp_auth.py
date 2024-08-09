#!/usr/bin/env python3
"""Session Auth with expiration.
"""

from .session_auth import SessionAuth, getenv
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """Session Auth system with exipration
    """

    def __init__(self):
        """Instantiates class instance.
        """

        try:
            self.session_duration = int(getenv('SESSION_DURATION', '0'))
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """Creates session for user.
        Overloads its super method
        """

        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
                }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """get user_id for the specified user id.
        Return
          - user_id
          - None id user_id is not found or if session_id not found
        """

        if session_id is None:
            return None
        if session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)

        if not session_dict or 'created_at' not in session_dict:
            return None
        expiration = session_dict.get('created_at')
        expiration += timedelta(seconds=self.session_duration)

        if expiration < datetime.now() and self.session_duration != 0:
            print("Session Expired")
            return None
        return session_dict.get('user_id')
