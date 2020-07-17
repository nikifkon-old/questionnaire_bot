import flask_login as login

from tbot.models import Account
from tbot.utils import session_scope


# Initialize flask-login
def init_login(app):
    with session_scope() as session:
        login_manager = login.LoginManager()
        login_manager.init_app(app)

        # Create user loader function
        @login_manager.user_loader
        def load_user(user_id):
            return session.query(Account).get(user_id)
