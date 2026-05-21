from flask import request, jsonify, current_app
from app.models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from app.routes import auth_bp
from app.utils.jwt_utils import generate_token


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User signup"""
    data = request.get_json()

    if not data.get('email') or not data.get('password') or not data.get('username'):
        return jsonify({'error': 'Missing required fields'}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400

    user = User(
        email=data['email'],
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        full_name=data.get('full_name', '')
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'message': 'User created successfully',
        'user_id': user.id
    }), 201


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login - returns JWT on success"""
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'error': 'Missing credentials'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if not user or not check_password_hash(user.password_hash, data['password']):
        return jsonify({'error': 'Invalid email or password'}), 401

    token = generate_token(user.id)

    return jsonify({
        'access_token': token,
        'token_type': 'bearer',
        'user': {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'full_name': user.full_name
        }
    }), 200
