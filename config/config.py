# config/config.py

import os


class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')
    DEBUG = False
    TESTING = False
    STATIC_FOLDER = 'static'
    TEMPLATES_FOLDER = 'templates'

    # Example API key
    API_KEY = os.environ.get('API_KEY', 'your_default_api_key')

    # File Paths
    DATA_FOLDER = os.path.join(os.getcwd(), 'test_data')

    # Add other base configurations here


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'
    # Additional development-specific config
    DATABASE_URI = 'sqlite:///dev_database.db'


class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    ENV = 'testing'
    DATABASE_URI = 'sqlite:///test_database.db'


class ProductionConfig(Config):
    """Production configuration."""
    ENV = 'production'
    DATABASE_URI = os.environ.get('PRODUCTION_DATABASE_URI')
    # Add other production-specific config


# Usage helper function
def get_config(env=None):
    config_mapping = {
        'development': DevelopmentConfig,
        'testing': TestingConfig,
        'production': ProductionConfig,
    }
    return config_mapping.get(env, Config)
