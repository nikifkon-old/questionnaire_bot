import os
import dotenv

from distutils.util import strtobool

dotenv.load_dotenv()


class Config:
    TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
    USE_POLLING = bool(strtobool(os.getenv("USE_POLLING", "False")))
    PUBLIC_KEY = os.getenv("PUBLIC_KEY", None)

    HOST = os.getenv("HOST")
    WEBHOOK_PATH = "/webhook/" + TELEGRAM_TOKEN
    WEBHOOK_URL = f"{HOST}{WEBHOOK_PATH}"

    WEBAPP_HOST = "0.0.0.0"
    WEBAPP_PORT = os.getenv("WEBAPP_PORT", 8000)
    WEBHOOK_PORT = os.getenv("WEBHOOK_PORT", 8001)

    DATABASE_HOST = os.getenv("DATABASE_HOST")
    DATABASE_PORT = os.getenv("DATABASE_PORT")
    DATABASE_USERNAME = os.getenv("DATABASE_USERNAME")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    DATABASE_NAME = os.getenv("DATABASE_NAME")

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")
    REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", None)

    FLASK_DEBUG = os.getenv("FLASK_DEBUG", 0)
    SECRET_KEY = os.getenv("SECRET_KEY")

    ADMIN_LOGIN = os.getenv("ADMIN_LOGIN", "admin")
    ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin")
