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

        return normalized_path not in normalized_excluded_paths

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
