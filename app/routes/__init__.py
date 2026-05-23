from flask import Blueprint, jsonify

api_bp = Blueprint("api", __name__, url_prefix="/api")
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


@api_bp.route("/health", methods=["GET"])
def health():
    """Health check endpoint."""

    return jsonify({
        "status": "ok",
        "service": "Sensus API",
    }), 200


from app.routes import accounts, analysis, auth, demo, ml, posts
