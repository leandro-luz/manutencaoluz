from datetime import timedelta


class Config(object):
    SECRET_KEY = "123"
    PERMANENT_SESSION_LIFETIME = timedelta(hours=2)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    MAIL_SERVER = 'smtp-mail.outlook.com'
    MAIL_PORT = 587
    MAIL_SENDER = 'Time Manutenção Luz <manutencaoluz@outlook.com>'
    MAIL_USERNAME = 'manutencaoluz@outlook.com'
    MAIL_PASSWORD = 'Aaa-11111'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class ProdConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql://bbc6cd19f46ca6:866f1a3b@us-cdbr-east-06.cleardb.net/heroku_dd95a3d8007484b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local_teste"
