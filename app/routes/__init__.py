from flask import Blueprint, jsonify

api_bp = Blueprint('api', __name__, url_prefix='/api')
auth_bp = Blueprint('auth', __name__, url_prefix='/api/auth')

# Health check endpoint
@api_bp.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok',
        'service': 'Instagram Analytics API'
    }), 200

# Importar rotas DEPOIS de criar os blueprints
from app.routes import auth, accounts, posts, analysis, ml
