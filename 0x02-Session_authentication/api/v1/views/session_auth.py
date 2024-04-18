#!/usr/bin/env python3
"""
session_auth.py
"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
import os


@app_views.route("/auth_session/login",
                 methods=["POST"], strict_slashes=False)
def login():
    """
    login
    """
    email = request.form.get("email")
    password = request.form.get("password")

    if not email or email == "":
        return jsonify({"error": "email missing"}), 400

    if not password or password == "":
        return jsonify({"error": "password missing"}), 400

    user = None

    try:
        user = User.search({"email": email})[0]
    except (Exception):
        pass

    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth

    session_id = auth.create_session(user.id)

    SESSION_NAME = os.getenv("SESSION_NAME")

    response = jsonify(user.to_json())
    response.set_cookie(SESSION_NAME, session_id)

    return response
