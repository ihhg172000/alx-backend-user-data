#!/usr/bin/env python3
"""
session_db_auth.py
"""
from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from uuid import uuid4
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """
    SessionDBAuth
    """
    def create_session(self, user_id=None):
        """
        create_session
        """
        session_id = str(uuid4())
        session = UserSession(user_id=user_id, session_id=session_id)
        session.save()

        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        user_id_for_session_id
        """
        if session_id is None:
            return None

        session = None

        try:
            UserSession.load_from_file()
            session = UserSession.search({"session_id": session_id})[0]
        except (Exception):
            pass

        if session is None:
            return None

        print(session)

        if self.session_duration == 0:
            return session.get("user_id")

        user_id = session.user_id
        created_at = session.created_at

        if created_at is None:
            return None

        if (created_at + timedelta(seconds=self.session_duration)
                < datetime.now()):
            return None

        return user_id

    def destroy_session(self, request=None):
        """
        destroy_session
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)

        if session_id is None:
            return False

        session = None

        try:
            session = UserSession.search({"session_id": session_id})[0]
        except (Exception):
            pass

        if session is None:
            return False

        session.remove()

        return True
