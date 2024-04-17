#!/usr/bin/env python3
"""
session_auth.py
"""
from api.v1.auth.auth import Auth
from uuid import uuid4
from models.user import User


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
            session_id = str(uuid4())
            SessionAuth.user_id_by_session_id[session_id] = user_id

            return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        user_id_for_session_id
        """
        if type(session_id) is str:
            return SessionAuth.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        current_user
        """
        session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(session_id)

        return User.get(user_id)
