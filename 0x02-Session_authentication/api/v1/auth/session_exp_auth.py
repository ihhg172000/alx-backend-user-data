#!/usr/bin/env python3
"""
session_exp_auth.py
"""
from flask.app import timedelta
from api.v1.auth.session_auth import SessionAuth
from datetime import datetime
import os


class SessionExpAuth(SessionAuth):
    user_id_by_session_id = {}

    def __init__(self) -> None:
        """
        __init__
        """
        super().__init__()

        try:
            self.session_duration = int(os.getenv("SESSION_DURATION"))
        except (Exception):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        create_session
        """
        session_id = super().create_session(user_id)

        if session_id is None:
            return None

        SessionExpAuth.user_id_by_session_id[session_id] = {
            "user_id": user_id,
            "created_at": datetime.now()
        }

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user_id_for_session_id
        """
        if session_id is None:
            return None

        session = SessionExpAuth.user_id_by_session_id.get(session_id)

        if session is None:
            return None

        if self.session_duration == 0:
            return session.get("user_id")

        user_id = session.get("user_id")
        created_at = session.get("created_at")

        if created_at is None:
            return None

        if (created_at + timedelta(seconds=self.session_duration)
                < datetime.now()):
            return None

        return user_id
