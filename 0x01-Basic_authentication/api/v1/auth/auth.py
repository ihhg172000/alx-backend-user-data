#!/usr/bin/env python3
"""
auth.py
"""
from flask import request
from typing import List, TypeVar


class Auth:
    """
    Auth
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        require_auth
        """
        if path and excluded_paths:
            path = path if path.endswith("/") else (path + "/")

            for excluded_path in excluded_paths:
                if excluded_path.endswith("*"):
                    if path.startswith(excluded_path[:-1]):
                        return False

                if path == excluded_path:
                    return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        authorization_header
        """
        if request:
            return request.headers.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """
        current_user
        """
        pass
