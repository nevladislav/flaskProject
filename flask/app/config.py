import sqlalchemy


class Configuration(object):
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:123456@localhost/Test'
    SECRET_KEY = 'secret'

    # flask-security
    #SECURITY_PASSWORD_SALT = 'salt'
    #SECURITY_PASSWORD_HASH = 'sha256_crypt'