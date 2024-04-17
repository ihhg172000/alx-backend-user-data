#!/usr/bin/env python3
"""
session_auth.py
"""
from api.v1.auth.auth import Auth
from uuid import uuid4


class SessionAuth(Auth):
    """
    SessionAuth
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        create_session
        """
        if type(user_id) is str:
            session_id = uuid4()
            SessionAuth.user_id_by_session_id[session_id] = user_id

            return session_id
