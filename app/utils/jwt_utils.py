import jwt
from datetime import datetime, timedelta
from flask import current_app, request, jsonify, g
from functools import wraps
from app.models import User


def generate_token(user_id: int):
    secret = current_app.config.get('JWT_SECRET_KEY')
    expires = current_app.config.get('JWT_ACCESS_TOKEN_EXPIRES')
    if not expires:
        expires = timedelta(hours=1)

    payload = {
        'user_id': user_id,
        'exp': datetime.utcnow() + expires
    }

    token = jwt.encode(payload, secret, algorithm='HS256')
    # PyJWT 2.x returns str for encode
    if isinstance(token, bytes):
        token = token.decode('utf-8')
    return token


def decode_token(token: str):
    secret = current_app.config.get('JWT_SECRET_KEY')
    try:
        payload = jwt.decode(token, secret, algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get('Authorization', None)
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({'error': 'Authorization header missing or invalid'}), 401

        token = auth_header.split(' ', 1)[1].strip()
        payload = decode_token(token)
        if not payload:
            return jsonify({'error': 'Invalid or expired token'}), 401

        user = User.query.get(payload.get('user_id'))
        if not user:
            return jsonify({'error': 'User not found'}), 401

        # Attach user to flask.g for downstream handlers
        g.current_user = user
        return func(*args, **kwargs)

    return wrapper
