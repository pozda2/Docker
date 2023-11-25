import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    # databáze se nastaví podle systémové provměnné DATABASE_URL z .environment
    # pokud není nastavená, použije se sqlite databáze
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite://")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
