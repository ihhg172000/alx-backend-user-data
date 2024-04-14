#!/usr/bin/env python3
"""
encrypt_password.py
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ hash_password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
