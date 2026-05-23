from flask import Flask
from flask_cors import CORS

from app.models import db
from config import get_config


def create_app():
    """Application factory."""

    config = get_config()
    app = Flask(__name__)
    app.config.from_object(config)

    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()

    from app.routes import api_bp, auth_bp
    from app.routes.web import web_bp

    app.register_blueprint(api_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(web_bp)

    return app
