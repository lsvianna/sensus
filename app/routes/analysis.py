from flask import request, jsonify
from app.models import db, Analysis, Post, InstagramAccount
from app.routes import api_bp

@api_bp.route('/accounts/<int:account_id>/analytics', methods=['GET'])
def get_account_analytics(account_id):
    """Get account analytics"""
    account = InstagramAccount.query.get(account_id)
    
    if not account:
        return jsonify({'error': 'Account not found'}), 404
    
    posts = Post.query.filter_by(account_id=account_id).all()
    
    if not posts:
        return jsonify({
            'account_id': account_id,
            'total_posts': 0,
            'average_engagement': 0,
            'sentiment_breakdown': {}
        }), 200
    
    total_engagement = sum(p.engagement_rate for p in posts) / len(posts) if posts else 0
    
    sentiment_counts = {
        'positive': len([p for p in posts if p.sentiment_label == 'positive']),
        'negative': len([p for p in posts if p.sentiment_label == 'negative']),
        'neutral': len([p for p in posts if p.sentiment_label == 'neutral'])
    }
    
    return jsonify({
        'account_id': account_id,
        'total_posts': len(posts),
        'average_engagement': total_engagement,
        'sentiment_breakdown': sentiment_counts,
        'total_likes': sum(p.likes_count for p in posts),
        'total_comments': sum(p.comments_count for p in posts)
    }), 200

@api_bp.route('/posts/<int:post_id>/analysis', methods=['GET'])
def get_post_analysis(post_id):
    """Get post analysis"""
    analysis = Analysis.query.filter_by(post_id=post_id).first()
    
    if not analysis:
        return jsonify({'error': 'Analysis not found'}), 404
    
    return jsonify({
        'post_id': analysis.post_id,
        'total_comments': analysis.total_comments,
        'positive_comments': analysis.positive_comments,
        'negative_comments': analysis.negative_comments,
        'neutral_comments': analysis.neutral_comments,
        'average_sentiment': analysis.average_sentiment,
        'engagement_trend': analysis.engagement_trend,
        'hashtags': analysis.hashtags,
        'mentions': analysis.mentions,
        'top_keywords': analysis.top_keywords
    }), 200
