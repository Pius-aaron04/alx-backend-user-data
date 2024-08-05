#!/usr/bin/env python3
"""Auth definitions"""
from .auth import Auth
import base64
import binascii
from typing import TypeVar
from models.user import User


class BasicAuth(Auth):
    """Basic Auth
    """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """Extracts Authorization header value
        """
        if not isinstance(authorization_header, str) or not\
           authorization_header.startswith('Basic ') or not\
           authorization_header:
            return None

        return authorization_header.lstrip('Basic ')

    def extract_user_credentials(self,
                                 decoded_base64_authorization_header: str) ->\
                                (str, str):
        """Fetches user's credentials.
        """

        if not decoded_base64_authorization_header or\
           not isinstance(decoded_base64_authorization_header, str) or\
           ':' not in decoded_base64_authorization_header:
            return None, None

        return tuple(decoded_base64_authorization_header.split(':'))

    def decode_base64_authorization_header(self,
                                           base64_authorization_header: str)\
            -> str:
        """decodes auth header
        """
        base64_auth = base64_authorization_header

        if base64_auth is None or not isinstance(base64_auth, str):
            return None
        try:
            header = base64.b64decode(base64_auth).decode('utf-8')
            return header
        except Exception:
            return None

    def user_object_from_credentials(self, user_email: str, user_pwd: str)\
            -> TypeVar('User'):
        """Gets user based on credentials.
        """

        if user_email is None or user_pwd is None:
            return None
        elif not isinstance(user_email, str) or not isinstance(user_pwd, str):
            return None
        search_list = User.search({
            "email": user_email
            })
        if len(search_list) == 0:
            return None
        for user in search_list:
            if user.is_valid_password(user_pwd):
                return user
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """gets current user object.
        """
        auth_header = self.authorization_header(request)
        auth_header = self.extract_base64_authorization_header(auth_header)
        decoded = self.decode_base64_authorization_header(auth_header)
        user_credentials = self.extract_user_credentials(decoded)

        user = self.user_object_from_credentials(*user_credentials)
        return user
