from werkzeug.security import check_password_hash
from wtforms import fields, form, validators

from tbot.models import Account
from tbot.utils import session_scope


# Define login and registration forms (for flask-login)
class LoginForm(form.Form):
    login = fields.StringField(validators=[validators.required()])
    password = fields.PasswordField(validators=[validators.required()])

    def validate_login(self, field):
        with session_scope() as session:
            user = self.get_user(session)

            if user is None:
                raise validators.ValidationError("Invalid user")

            # we're comparing the plaintext pw with the the hash from the db
            if not check_password_hash(user.password, self.password.data):
                # to compare plain text passwords use
                # if user.password != self.password.data:
                raise validators.ValidationError("Invalid password")

    def get_user(self, session):
        return session.query(Account).filter_by(login=self.login.data).first()
