import os

class Config(object):
    """Parent configuration class."""
    DEBUG = False
    CSRF_ENABLED = True
    COHORTS = ['r11', 'r12', 'r13', 'r14']
    ELASTIC_SEARCH_URL = os.getenv('ELASTIC_SEARCH_URL')

class DevelopmentConfig(Config):
    """Configurations for Development."""
    DEBUG = True
    ELASTIC_SEARCH_URL = 'http://localhost:9200'

class TestingConfig(Config):
    """Configurations for Testing, with a separate test database."""
    TESTING = True
    DEBUG = True    
    ELASTIC_SEARCH_URL = 'http://localhost:9200'

class ProductionConfig(Config):
    """Configurations for Production."""
    DEBUG = False
    TESTING = False
    ELASTIC_SEARCH_URL = os.getenv('ELASTIC_SEARCH_URL')

app_config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
}