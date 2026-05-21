from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from .models import User, InstagramAccount, Post, Comment, Analysis, MLExperiment
