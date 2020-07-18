import os

from werkzeug.security import generate_password_hash

from config import Config
from tbot.utils import session_scope
from tbot.models import Account


if __name__ == "__main__":
    with session_scope() as session:
        data = {
            "login": Config.ADMIN_LOGIN,
            "password": generate_password_hash(Config.ADMIN_PASSWORD)
        }
        acc = Account(**data)
        session.add(acc)
