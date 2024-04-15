#!/usr/bin/env python3
"""
basic_auth.py
"""
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """
    BasicAuth
    """
    def extract_base64_authorization_header(
            self, authorization_header: str) -> str:
        """
        extract_base64_authorization_header
        """
        if not authorization_header or type(authorization_header) is not str:
            return None

        if not authorization_header.startswith("Basic "):
            return None

        return authorization_header[6:]
