import os


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")

    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    FLASK_DEBUG = os.getenv("FLASK_DEBUG", 0)
    SECRET_KEY = os.getenv("SECRET_KEY")

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
