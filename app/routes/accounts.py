from flask import request, jsonify
from app.models import db, InstagramAccount, User
from app.routes import api_bp

@api_bp.route('/accounts', methods=['GET'])
def get_accounts():
    """List user's Instagram accounts"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id required'}), 400
    
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    accounts = InstagramAccount.query.filter_by(user_id=user_id).all()
    
    return jsonify({
        'accounts': [{
            'id': acc.id,
            'username': acc.username,
            'display_name': acc.display_name,
            'followers_count': acc.followers_count,
            'posts_count': len(acc.posts)
        } for acc in accounts]
    }), 200

@api_bp.route('/accounts', methods=['POST'])
def add_account():
    """Add Instagram account to monitor"""
    data = request.get_json()
    
    if not data.get('user_id') or not data.get('instagram_username'):
        return jsonify({'error': 'Missing required fields'}), 400
    
    user = User.query.get(data['user_id'])
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Check if already exists
    if InstagramAccount.query.filter_by(username=data['instagram_username']).first():
        return jsonify({'error': 'Account already monitored'}), 400
    
    account = InstagramAccount(
        user_id=data['user_id'],
        instagram_id=f"temp_{data['instagram_username']}",  # Will be replaced with real API call
        username=data['instagram_username'],
        display_name=data['instagram_username']
    )
    
    db.session.add(account)
    db.session.commit()
    
    return jsonify({
        'message': 'Account added',
        'account_id': account.id
    }), 201

@api_bp.route('/accounts/<int:account_id>', methods=['GET'])
def get_account(account_id):
    """Get account details"""
    account = InstagramAccount.query.get(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    return jsonify({
        'id': account.id,
        'username': account.username,
        'display_name': account.display_name,
        'followers_count': account.followers_count,
        'bio': account.bio,
        'posts_count': len(account.posts),
        'last_sync': account.last_sync.isoformat() if account.last_sync else None
    }), 200
