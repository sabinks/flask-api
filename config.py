import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default-secret")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "default-jwt-secret")
    DEBUG = False
    TESTING = False
    # MySQL connection string
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_NAME = os.getenv("DB_NAME")
    # Looking to send emails in production? Check out our Email API/SMTP product!
# Looking to send emails in production? Check out our Email API/SMTP product!
    MAIL_SERVER = os.getenv("MAIL_SERVER")
    MAIL_PORT = os.getenv("MAIL_PORT")
    MAIL_USERNAME = os.getenv("MAIL_USERNAME")
    MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_DEFAULT_SENDER= os.getenv('MAIL_DEFAULT_SENDER')

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False
    
class TestingConfig(Config):
    TESTING = True