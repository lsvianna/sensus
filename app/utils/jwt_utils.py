from datetime import timedelta
from functools import wraps

import jwt
from flask import current_app, g, jsonify, request

from app.models import User, db
from app.utils.time import utcnow


def generate_token(user_id: int):
    secret = current_app.config.get("JWT_SECRET_KEY")
    expires = current_app.config.get("JWT_ACCESS_TOKEN_EXPIRES") or timedelta(hours=1)

    payload = {
        "user_id": user_id,
        "exp": utcnow() + expires,
    }

    token = jwt.encode(payload, secret, algorithm="HS256")
    if isinstance(token, bytes):
        token = token.decode("utf-8")
    return token


def decode_token(token: str):
    secret = current_app.config.get("JWT_SECRET_KEY")
    try:
        return jwt.decode(token, secret, algorithms=["HS256"])
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        return None


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"error": "Authorization header missing or invalid"}), 401

        payload = decode_token(auth_header.split(" ", 1)[1].strip())
        if not payload:
            return jsonify({"error": "Invalid or expired token"}), 401

        user = db.session.get(User, payload.get("user_id"))
        if not user:
            return jsonify({"error": "User not found"}), 401

        g.current_user = user
        return func(*args, **kwargs)

    return wrapper
