from flask import Flask, request, jsonify, current_app
from flask_cors import CORS
from config import get_config
from app.models import db

def create_app():
    """Application factory"""
    config = get_config()
    app = Flask(__name__)
    app.config.from_object(config)
    
    # Initialize extensions
    db.init_app(app)
    CORS(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints
    from app.routes import api_bp, auth_bp
    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)

    return app
