# config.py
"""
Configuration management for CheatSheeter application.
"""

import os


class Config:
    """Base configuration with default values."""

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # File storage
    CHEATSHEETS_FOLDER = os.environ.get(
        "CHEATSHEETS_FOLDER", os.path.join(os.getcwd(), "cheatsheets")
    )

    # Server
    HOST = os.environ.get("FLASK_HOST", "0.0.0.0")
    PORT = int(os.environ.get("FLASK_PORT", 5000))

    # CORS
    ALLOWED_ORIGINS = (
        os.environ.get("ALLOWED_ORIGINS", "").split(",")
        if os.environ.get("ALLOWED_ORIGINS")
        else ["*"]
    )

    # Rate limiting
    RATELIMIT_STORAGE_URL = os.environ.get("RATELIMIT_STORAGE_URL", "memory://")

    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")


class DevelopmentConfig(Config):
    """Development environment configuration."""

    DEBUG = True
    TESTING = False
    ENV = "development"


class ProductionConfig(Config):
    """Production environment configuration."""

    DEBUG = False
    TESTING = False
    ENV = "production"

    # Override with secure defaults for production
    ALLOWED_ORIGINS = os.environ.get("ALLOWED_ORIGINS", "http://localhost:8080").split(
        ","
    )


class TestingConfig(Config):
    """Testing environment configuration."""

    DEBUG = True
    TESTING = True
    ENV = "testing"
    CHEATSHEETS_FOLDER = os.path.join(os.getcwd(), "test_cheatsheets")


# Configuration dictionary
config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    "default": DevelopmentConfig,
}
