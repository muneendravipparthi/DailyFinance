import os

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Flask settings
    DEBUG = True
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')

    # Database settings
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'data.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Additional settings (e.g., Cross-Origin Resource Sharing)
    CORS_HEADERS = 'Content-Type'
