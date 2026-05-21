import os
import requests
import logging
from typing import Dict, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

class InstagramService:
    """
    Service for interacting with Instagram Graph API
    """
    
    def __init__(self):
        self.base_url = os.getenv('INSTAGRAM_GRAPH_API_BASE_URL', 'https://graph.instagram.com')
        self.api_version = os.getenv('INSTAGRAM_API_VERSION', 'v18.0')
        self.access_token = os.getenv('INSTAGRAM_ACCESS_TOKEN')
        self.business_account_id = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID')
    
    def get_account_info(self, instagram_username: str) -> Optional[Dict]:
        """
        Get Instagram account info (requires public data access)
        For MVP, we'll return mock data
        """
        try:
            # In production, you would call the real API
            # For now, return mock data for testing
            return {
                'instagram_id': f'mock_{instagram_username}',
                'username': instagram_username,
                'name': instagram_username.title(),
                'biography': 'Mock biography for testing',
                'profile_picture_url': f'https://via.placeholder.com/150',
                'followers_count': 1000,
                'following_count': 500
            }
        except Exception as e:
            logger.error(f"Error getting account info: {e}")
            return None
    
    def get_posts(self, account_id: str, limit: int = 20) -> List[Dict]:
        """
        Get recent posts from an Instagram account
        """
        try:
            # Mock data for MVP
            mock_posts = [
                {
                    'id': f'post_{i}',
                    'caption': f'Sample post {i}',
                    'media_type': 'IMAGE',
                    'media_url': f'https://via.placeholder.com/400',
                    'likes_count': 100 + i * 10,
                    'comments_count': 10 + i,
                    'timestamp': datetime.utcnow().isoformat()
                }
                for i in range(limit)
            ]
            return mock_posts
        except Exception as e:
            logger.error(f"Error getting posts: {e}")
            return []
    
    def get_comments(self, post_id: str, limit: int = 100) -> List[Dict]:
        """
        Get comments from a post
        """
        try:
            # Mock data
            mock_comments = [
                {
                    'id': f'comment_{i}',
                    'text': f'Great content! Comment {i}',
                    'username': f'user_{i}',
                    'likes_count': i,
                    'timestamp': datetime.utcnow().isoformat()
                }
                for i in range(limit)
            ]
            return mock_comments
        except Exception as e:
            logger.error(f"Error getting comments: {e}")
            return []
    
    def sync_account(self, account_id: str) -> bool:
        """
        Sync Instagram account data with database
        """
        try:
            logger.info(f"Syncing account {account_id}")
            # In production, this would fetch real data and update the database
            return True
        except Exception as e:
            logger.error(f"Error syncing account: {e}")
            return False
