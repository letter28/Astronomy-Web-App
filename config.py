import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SECRET_KEY = 'coffee'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'astronomy.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

