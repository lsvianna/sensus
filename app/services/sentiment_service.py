import logging
import re
from typing import Dict, Tuple, List
from textblob import TextBlob
import numpy as np

logger = logging.getLogger(__name__)

class SentimentService:
    """
    Service for sentiment analysis of text
    Uses TextBlob for lightweight sentiment analysis
    """
    
    def __init__(self):
        self.positive_threshold = 0.1
        self.negative_threshold = -0.1
    
    def analyze_text(self, text: str) -> Dict:
        """
        Analyze sentiment of text
        
        Returns:
        {
            'score': float (-1 to 1),
            'label': str (positive, negative, neutral),
            'polarity': float,
            'subjectivity': float
        }
        """
        try:
            if not text or len(text.strip()) == 0:
                return {
                    'score': 0.0,
                    'label': 'neutral',
                    'polarity': 0.0,
                    'subjectivity': 0.0
                }
            
            # Clean text
            cleaned_text = self._clean_text(text)
            
            # Analyze
            blob = TextBlob(cleaned_text)
            polarity = blob.sentiment.polarity
            subjectivity = blob.sentiment.subjectivity
            
            # Classify
            if polarity > self.positive_threshold:
                label = 'positive'
            elif polarity < self.negative_threshold:
                label = 'negative'
            else:
                label = 'neutral'
            
            return {
                'score': polarity,
                'label': label,
                'polarity': polarity,
                'subjectivity': subjectivity
            }
        except Exception as e:
            logger.error(f"Error analyzing sentiment: {e}")
            return {
                'score': 0.0,
                'label': 'neutral',
                'polarity': 0.0,
                'subjectivity': 0.0
            }
    
    def extract_hashtags(self, text: str) -> List[str]:
        """Extract hashtags from text"""
        hashtags = re.findall(r'#\w+', text)
        return hashtags
    
    def extract_mentions(self, text: str) -> List[str]:
        """Extract mentions from text"""
        mentions = re.findall(r'@\w+', text)
        return mentions
    
    def extract_keywords(self, text: str, top_n: int = 10) -> List[Tuple[str, int]]:
        """
        Extract keywords from text
        Simple implementation: split, clean, count
        """
        try:
            # Remove URLs, mentions, hashtags
            text = re.sub(r'http\S+|@\w+|#\w+', '', text, flags=re.MULTILINE)
            
            # Split into words
            words = text.lower().split()
            
            # Filter short words and common words
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were',
                'be', 'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will',
                'would', 'could', 'should', 'may', 'might', 'can', 'of', 'in',
                'to', 'for', 'on', 'with', 'by', 'from', 'as', 'at', 'it', 'this',
                'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they'
            }
            
            filtered_words = [w for w in words if len(w) > 3 and w not in stop_words]
            
            # Count and return top N
            from collections import Counter
            word_counts = Counter(filtered_words)
            return word_counts.most_common(top_n)
        except Exception as e:
            logger.error(f"Error extracting keywords: {e}")
            return []
    
    def analyze_comments_batch(self, comments: List[str]) -> Dict:
        """
        Analyze multiple comments and return aggregate stats
        """
        try:
            results = [self.analyze_text(comment) for comment in comments]
            
            positive = len([r for r in results if r['label'] == 'positive'])
            negative = len([r for r in results if r['label'] == 'negative'])
            neutral = len([r for r in results if r['label'] == 'neutral'])
            
            avg_sentiment = np.mean([r['score'] for r in results]) if results else 0.0
            
            return {
                'total': len(results),
                'positive': positive,
                'negative': negative,
                'neutral': neutral,
                'average_sentiment': float(avg_sentiment),
                'sentiment_distribution': {
                    'positive': positive / len(results) * 100 if results else 0,
                    'negative': negative / len(results) * 100 if results else 0,
                    'neutral': neutral / len(results) * 100 if results else 0
                }
            }
        except Exception as e:
            logger.error(f"Error analyzing batch comments: {e}")
            return {
                'total': 0,
                'positive': 0,
                'negative': 0,
                'neutral': 0,
                'average_sentiment': 0.0,
                'sentiment_distribution': {}
            }
    
    def _clean_text(self, text: str) -> str:
        """Clean text for analysis"""
        # Remove URLs
        text = re.sub(r'http\S+|www\S+', '', text, flags=re.MULTILINE)
        # Remove HTML tags
        text = re.sub(r'<.*?>', '', text)
        # Remove extra whitespace
        text = ' '.join(text.split())
        return text
