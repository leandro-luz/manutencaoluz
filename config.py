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
    SQLALCHEMY_DATABASE_URI = 'mysql://{username}:{password}@{hostname}/{databasename}'.format(
        username="manutencaoluz",
        password="aaa11111",
        hostname="manutencaoluz.mysql.pythonanywhere-services.com",
        databasename="manutencaoluz$manutencaoluz_prod",
    )
    SQLALCHMEY_POOL_RECYCLE = 299
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local"


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local_teste"
