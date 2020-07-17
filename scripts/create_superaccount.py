import os

from werkzeug.security import generate_password_hash

from tbot.utils import session_scope
from tbot.models import Account


if __name__ == "__main__":
    with session_scope() as session:
        data = {
            "login": os.environ.get("ADMIN_LOGIN"),
            "password": generate_password_hash(os.environ.get("ADMIN_PASSWORD"))
        }
        acc = Account(**data)
        session.add(acc)
