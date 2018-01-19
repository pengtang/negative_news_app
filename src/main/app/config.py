import os


class BaseConfig(object):
    DEBUG = False
    SECRET_KEY = '\x04w_\x00\xdb9\xb5l\xc6\xb4\x0c\x86\xf5h\xeb\xb9\xf1\x92\xebR\x0c\xa6\x16\x18'
    # Get environment variable DATABASE_URL from command "heroku config | grep HEROKU_POSTGRESQL"
    # Then export the variable DATABASE_URL from previous value
    # SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ARTICLE_TABLE_NAME = 'related_articles'


class DevelopmentConfig(BaseConfig):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost:5432'


class CloudConfig(BaseConfig):
    DEBUG = False
