class Config(object):
    SECRET_KEY = "123"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = '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'
    MAIL_FROM = 'guguleo2019@gmail.com'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://bbc6cd19f46ca6:866f1a3b@us-cdbr-east-06.cleardb.net/heroku_dd95a3d8007484b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local_teste"
