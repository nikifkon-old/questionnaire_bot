from config import Config
from tbot.models import Account
from tbot.utils import session_scope

if __name__ == "__main__":
    with session_scope() as session:
        data = {
            "login": Config.ADMIN_LOGIN
        }
        acc = Account(**data)
        acc.set_password(Config.ADMIN_PASSWORD)
        session.add(acc)
