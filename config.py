import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string'
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = '712640388@qq.com'
    MAIL_PASSWORD = 'cecfgtlembsjbbce'
    FLASKY_MAIL_SUBJEXT_PREFIX = '[平梵]'
    FLASKY_MAIL_SENDER = '712640388@qq.com'
    FLASKY_ADMIN = '712640388@qq.com'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    FLASKY_POSTS_PER_PAGE = 20
    FLASKY_FOLLOWERS_PER_PAGE = 50
    FLASKY_COMMENTS_PER_PAGE = 30
    FLASKY_SLOW_DB_QUERY_TIME = 0.5

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get('DEV_DATABASE_URL') or \
        'mysql://' + os.path.join(basedir, 'data-dev.mysql')


class TestingConfig(Config):
    TESTINF = True
    DEBUG = True
    # SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or \
    #                           'mysql://'

    SQLALCHEMY_DATABASE_URI = 'mysql://web:web@localhost/web'
    #print(SQLALCHEMY_DATABASE_URI)


class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql:///' + os.path.join(basedir, 'data.mysql')


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}