import os
basedir = os.path.abspath(os.path.dirname(__file__))

#  Config class for SQLAlchemy
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = 'mysql://root:Secretpassword@mariadb-app:3306/app'
    SQLALCHEMY_TRACK_MODIFICATIONS = False