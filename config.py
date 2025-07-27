import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Base configuration class."""

    SECRET_KEY = os.getenv("SECRET_KEY")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    """Development configuration."""

    SQLALCHEMY_DATABASE_URI = os.getenv("DEV_DATABASE_URI")
    DEBUG = True


class TestConfig(Config):
    """Testing configuration."""

    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    TESTING = True
    WTF_CSRF_ENABLED = False
