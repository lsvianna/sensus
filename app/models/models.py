from datetime import datetime
from app.models import db

class User(db.Model):
    """Usuário da plataforma"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(120))
    plan = db.Column(db.String(20), default='free')  # free, pro, enterprise
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    accounts = db.relationship('InstagramAccount', back_populates='user', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'


class InstagramAccount(db.Model):
    """Conta do Instagram monitorada"""
    __tablename__ = 'instagram_accounts'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    instagram_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), nullable=False)
    display_name = db.Column(db.String(120))
    bio = db.Column(db.Text)
    profile_picture_url = db.Column(db.String(500))
    followers_count = db.Column(db.Integer, default=0)
    following_count = db.Column(db.Integer, default=0)
    last_sync = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    user = db.relationship('User', back_populates='accounts')
    posts = db.relationship('Post', back_populates='account', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<InstagramAccount {self.username}>'


class Post(db.Model):
    """Post do Instagram"""
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    account_id = db.Column(db.Integer, db.ForeignKey('instagram_accounts.id'), nullable=False)
    instagram_id = db.Column(db.String(50), unique=True, nullable=False, index=True)
    caption = db.Column(db.Text)
    media_url = db.Column(db.String(500))
    media_type = db.Column(db.String(20))  # IMAGE, VIDEO, CAROUSEL
    likes_count = db.Column(db.Integer, default=0)
    comments_count = db.Column(db.Integer, default=0)
    engagement_rate = db.Column(db.Float, default=0.0)
    sentiment_score = db.Column(db.Float)  # -1 a 1
    sentiment_label = db.Column(db.String(20))  # positive, negative, neutral
    posted_at = db.Column(db.DateTime, nullable=False, index=True)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    account = db.relationship('InstagramAccount', back_populates='posts')
    comments = db.relationship('Comment', back_populates='post', cascade='all, delete-orphan')
    analysis = db.relationship('Analysis', back_populates='post', uselist=False, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Post {self.instagram_id}>'


class Comment(db.Model):
    """Comentário em um post"""
    __tablename__ = 'comments'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False)
    instagram_id = db.Column(db.String(50), unique=True, nullable=False)
    author_username = db.Column(db.String(80))
    text = db.Column(db.Text, nullable=False)
    likes_count = db.Column(db.Integer, default=0)
    sentiment_score = db.Column(db.Float)  # -1 a 1
    sentiment_label = db.Column(db.String(20))  # positive, negative, neutral
    created_at = db.Column(db.DateTime, nullable=False, index=True)
    fetched_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    post = db.relationship('Post', back_populates='comments')
    
    def __repr__(self):
        return f'<Comment {self.instagram_id}>'


class Analysis(db.Model):
    """Análise agregada de um post"""
    __tablename__ = 'analysis'
    
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), nullable=False, unique=True)
    total_comments = db.Column(db.Integer, default=0)
    positive_comments = db.Column(db.Integer, default=0)
    negative_comments = db.Column(db.Integer, default=0)
    neutral_comments = db.Column(db.Integer, default=0)
    average_sentiment = db.Column(db.Float)
    engagement_trend = db.Column(db.String(20))  # rising, stable, falling
    hashtags = db.Column(db.JSON)
    mentions = db.Column(db.JSON)
    top_keywords = db.Column(db.JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    post = db.relationship('Post', back_populates='analysis')
    
    def __repr__(self):
        return f'<Analysis Post:{self.post_id}>'


class MLExperiment(db.Model):
    """Metadata for ML experiments / training runs"""
    __tablename__ = 'ml_experiments'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    params = db.Column(db.JSON)
    metrics = db.Column(db.JSON)
    status = db.Column(db.String(30), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<MLExperiment {self.name}>'
