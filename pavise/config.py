import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    """Base configuration"""
    
    database = os.environ["APPLICATION_DB"]

class ProductionConfig(Config):
    """Production configuration"""

class DevelopmentConfig(Config):
    """Development configuration"""


class TestingConfig(Config):
    """Testing configuration"""

    TESTING = True
