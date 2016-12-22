import os


class Config(object):
    DEBUG = False
    TESTING = False
    SERVER_NAME = 'localhost:5000'
    SECRET_KEY = (
        'neigh6echeih4eiqueetei2ietha1raitooSahzai6ugh0jahzahm'
        'u2»{1³21igh1saWooshi3uxah4oongiuphiox7iephoonahkoiK9u'
    )

    # Flask-SQLAlchemy options (see http://flask-sqlalchemy.pocoo.org/2.1/config/)
    SQLALCHEMY_DATABASE_URI = os.environ['SQLALCHEMY_DATABASE_URI']
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    PASSLIB_SCHEMES = ["argon2"]


class ProductionConfig(Config):
    pass


class StagingConfig(Config):
    pass


class TestingConfig(Config):
    TESTING = True


class DevelopConfig(Config):
    SQLALCHEMY_ECHO = True


configs = {
    'production': ProductionConfig,
    'staging': StagingConfig,
    'testing': TestingConfig,
    'develop': DevelopConfig,
}