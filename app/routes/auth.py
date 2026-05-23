from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, User
from app.routes import auth_bp
from app.utils.jwt_utils import generate_token


@auth_bp.route("/signup", methods=["POST"])
def signup():
    """Create a user account."""

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    username = (data.get("username") or "").strip()
    password = data.get("password") or ""

    if not email or not password or not username:
        return jsonify({"error": "email, username and password are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 400

    user = User(
        email=email,
        username=username,
        password_hash=generate_password_hash(password),
        full_name=data.get("full_name", ""),
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": user.id}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    """User login - returns JWT on success."""

    data = request.get_json(silent=True) or {}
    email = (data.get("email") or "").strip().lower()
    password = data.get("password") or ""

    if not email or not password:
        return jsonify({"error": "email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    token = generate_token(user.id)

    return jsonify({
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": user.id,
            "email": user.email,
            "username": user.username,
            "full_name": user.full_name,
        },
    }), 200
