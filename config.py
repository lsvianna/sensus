import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
DEFAULT_SQLITE_PATH = BASE_DIR / "instance" / "instagram_analytics.db"


def normalize_database_url(value):
    if not value:
        return f"sqlite:///{DEFAULT_SQLITE_PATH.as_posix()}"

    if value.startswith("postgres://"):
        return value.replace("postgres://", "postgresql+psycopg://", 1)

    return value


def env_bool(name, default=False):
    value = os.getenv(name)
    if value is None:
        return default
    return value.lower() in {"1", "true", "yes", "on"}


class Config:
    """Base configuration."""

    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "dev-jwt-secret-change-before-prod-123456")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=30)

    INSTAGRAM_API_VERSION = os.getenv("INSTAGRAM_API_VERSION", "v18.0")
    INSTAGRAM_GRAPH_API_BASE_URL = "https://graph.instagram.com"


class DevelopmentConfig(Config):
    """Development configuration for Windows and Codespaces."""

    DEBUG = True
    TESTING = False
    SQLALCHEMY_ECHO = env_bool("SQLALCHEMY_ECHO", False)
    SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv("DATABASE_URL"))


class TestingConfig(Config):
    """Testing configuration."""

    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(Config):
    """Production configuration."""

    DEBUG = False
    TESTING = False
    SQLALCHEMY_ECHO = env_bool("SQLALCHEMY_ECHO", False)
    SQLALCHEMY_DATABASE_URI = normalize_database_url(os.getenv("DATABASE_URL"))


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
    "default": DevelopmentConfig,
}


def get_config():
    """Get config based on FLASK_ENV."""

    env = os.getenv("FLASK_ENV", "development")
    return config_by_name.get(env, DevelopmentConfig)
