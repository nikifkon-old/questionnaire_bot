from config import Config
from tbot.utils import session_scope
from tbot.models import Account


if __name__ == "__main__":
    with session_scope() as session:
        data = {
            "login": Config.ADMIN_LOGIN
        }
        acc = Account(**data)
        acc.set_password(Config.ADMIN_PASSWORD)
        session.add(acc)
