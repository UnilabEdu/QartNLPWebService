import os
basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):

    # Flask settings
    CSRF_ENABLED = True
    DEBUG = True

    # Flask-SQLAlchemy settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'appsecretkey')
    SQLALCHEMY_DATABASE_URI = os.environ.get('SQLALCHEMY_DATABASE_URI', f'sqlite:///{os.path.join(basedir, "data.db")}')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Celery settings
    UPLOAD_FOLDER = "app/uploads/"
    CELERY_BROKER_URL = "redis://localhost"
    CELERY_RESULT_BACKEND = "redis://localhost"

    # Flask-User settings
    USER_ENABLE_EMAIL = True
    MAIL_SERVER = 'smtp.mailtrap.io'
    MAIL_PORT = 2525
    MAIL_USERNAME = '9c35497ccc3adf'
    MAIL_PASSWORD = '729aadc701a4e7'
    MAIL_DEFAULT_SENDER = '9c35497ccc3adf'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    USER_ENABLE_CONFIRM_EMAIL = False

    # Flask-Babel settings
    LANGUAGES = {"en": "English",
                 "ka": "Georgian"}
