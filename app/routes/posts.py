from flask import request, jsonify
from app.models import db, Post, InstagramAccount
from app.routes import api_bp
from app.services.analysis_service import AnalysisService
from app.tasks.analysis_tasks import analyze_post_task, celery

@api_bp.route('/accounts/<int:account_id>/posts', methods=['GET'])
def get_posts(account_id):
    """Get posts from an account"""
    account = InstagramAccount.query.get(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    limit = request.args.get('limit', 10, type=int)
    posts = Post.query.filter_by(account_id=account_id).order_by(Post.posted_at.desc()).limit(limit).all()
    
    return jsonify({
        'posts': [{
            'id': p.id,
            'caption': p.caption,
            'likes_count': p.likes_count,
            'comments_count': p.comments_count,
            'engagement_rate': p.engagement_rate,
            'sentiment_label': p.sentiment_label,
            'sentiment_score': p.sentiment_score,
            'posted_at': p.posted_at.isoformat()
        } for p in posts]
    }), 200

@api_bp.route('/posts/<int:post_id>', methods=['GET'])
def get_post(post_id):
    """Get post details"""
    post = Post.query.get(post_id)
    
    if not post:
        return jsonify({'error': 'Post not found'}), 404
    
    return jsonify({
        'id': post.id,
        'caption': post.caption,
        'likes_count': post.likes_count,
        'comments_count': post.comments_count,
        'engagement_rate': post.engagement_rate,
        'sentiment_label': post.sentiment_label,
        'sentiment_score': post.sentiment_score,
        'posted_at': post.posted_at.isoformat(),
        'comments_count_analyzed': len(post.comments)
    }), 200


@api_bp.route('/posts/<int:post_id>/analyze', methods=['POST'])
def analyze_post(post_id):
    """Trigger analysis for a post. Uses Celery if configured, otherwise runs synchronously."""
    post = Post.query.get(post_id)
    if not post:
        return jsonify({'error': 'Post not found'}), 404

    # If Celery is available, enqueue task
    if celery:
        task = analyze_post_task.delay(post_id)
        return jsonify({'task_id': task.id, 'status': 'queued'}), 202

    # Fallback to synchronous analysis
    service = AnalysisService()
    result = service.analyze_post(post)
    if result.get('error'):
        return jsonify(result), 500
    return jsonify(result), 200
