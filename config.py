class Config(object):
    SECRET_KEY = "123"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENDGRID_API_KEY = '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'
    MAIL_FROM = 'guguleo2019@gmail.com'
    DEBUG_TB_INTERCEPT_REDIRECTS = False


class ProdConfig(Config):
    # SQLALCHEMY_DATABASE_URI = 'mysql://ba59712aa64752:bfe80c0c@us-cdbr-east-06.cleardb.net/heroku_4be8a3175e5b04d'
    SQLALCHEMY_DATABASE_URI = 'mysql://bbc6cd19f46ca6:866f1a3b@us-cdbr-east-06.cleardb.net/heroku_dd95a3d8007484b'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local"

    MAIL_KEY = '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'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 165
    MAIL_USERNAME = 'guguleo2019@gmail.com'
    MAIL_PASSWORD = 'Aaa-11111'


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = "mysql://root:@localhost/manutenção_luz_local_teste"
