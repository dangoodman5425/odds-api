import os


class BaseConfig:
    """Base configuration
    """
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv('SECRET_KEY')


class DevelopmentConfig(BaseConfig):
    """Development configuration
    """
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:password@localhost:5432'
    CACHE_TYPE = 'simple'
