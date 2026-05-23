from typing import List
import logging
from app.services.sentiment_service import SentimentService
from app.services.instagram_service import InstagramService
from app.models import db, Post, Comment, Analysis
from app.utils.time import utcnow

logger = logging.getLogger(__name__)


class AnalysisService:
    def __init__(self):
        self.sentiment = SentimentService()
        self.ig = InstagramService()

    def analyze_post(self, post: Post) -> dict:
        """Analyze a single post: fetch comments, analyze sentiments, store results."""
        try:
            # Fetch comments from Instagram (mock) if none in DB
            if post.comments and len(post.comments) > 0:
                comments_texts = [c.text for c in post.comments]
            else:
                comments = self.ig.get_comments(post.instagram_id, limit=200)
                comments_texts = [c.get('text', '') for c in comments]

            # Analyze comments
            batch_result = self.sentiment.analyze_comments_batch(comments_texts)

            # Create/Update Analysis row
            analysis = Analysis.query.filter_by(post_id=post.id).first()
            if not analysis:
                analysis = Analysis(post_id=post.id)

            analysis.total_comments = batch_result.get('total', 0)
            analysis.positive_comments = batch_result.get('positive', 0)
            analysis.negative_comments = batch_result.get('negative', 0)
            analysis.neutral_comments = batch_result.get('neutral', 0)
            analysis.average_sentiment = batch_result.get('average_sentiment', 0.0)

            # Extract hashtags/mentions from caption
            hashtags = self.sentiment.extract_hashtags(post.caption or '')
            mentions = self.sentiment.extract_mentions(post.caption or '')
            analysis.hashtags = hashtags
            analysis.mentions = mentions

            # Top keywords from caption + comments
            top_from_caption = self.sentiment.extract_keywords(post.caption or '', top_n=5)
            top_from_comments = self.sentiment.extract_keywords(' '.join(comments_texts), top_n=10)
            analysis.top_keywords = {
                'caption': top_from_caption,
                'comments': top_from_comments
            }

            # Simple engagement trend stub
            analysis.engagement_trend = 'stable'

            # Save analysis
            db.session.add(analysis)

            # Update post aggregate sentiment
            post.sentiment_score = analysis.average_sentiment
            if post.sentiment_score is None:
                post.sentiment_score = 0.0

            if post.sentiment_score > self.sentiment.positive_threshold:
                post.sentiment_label = 'positive'
            elif post.sentiment_score < self.sentiment.negative_threshold:
                post.sentiment_label = 'negative'
            else:
                post.sentiment_label = 'neutral'

            post.fetched_at = utcnow()

            db.session.add(post)
            db.session.commit()

            return {
                'post_id': post.id,
                'analysis': {
                    'total_comments': analysis.total_comments,
                    'positive_comments': analysis.positive_comments,
                    'negative_comments': analysis.negative_comments,
                    'neutral_comments': analysis.neutral_comments,
                    'average_sentiment': analysis.average_sentiment
                }
            }

        except Exception as e:
            logger.error(f"Error analyzing post {post.id}: {e}")
            db.session.rollback()
            return {'error': str(e)}
