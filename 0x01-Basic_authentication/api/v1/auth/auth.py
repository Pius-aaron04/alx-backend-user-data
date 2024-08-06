#!/usr/bin/env python3

"""Auth file"""

from flask import request
from typing import List, TypeVar


class Auth:
    """Auth class"""

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """Checks for auth"""
        if not path or not excluded_paths:
            return True

        normalized_path = path.rstrip('/')
        normalized_excluded_paths = {p.rstrip('/') for p in excluded_paths}

        for path_ in normalized_excluded_paths:
            if path_ == normalized_path:
                return False
            elif path_.endswith('*') and\
                    normalized_path.startswith(path_.rstrip('*')):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """Generates Authorization header
        """
        if request is None:
            return None

        if 'Authorization' not in request.headers:
            return None
        return request.headers['Authorization']

    def current_user(self, request=None) -> TypeVar('User'):
        """Checks ther current user
        """
        return None
