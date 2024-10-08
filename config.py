import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = "mysql+py" + os.environ.get("MYSQL_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
