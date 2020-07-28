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

            if not user.check_password(self.password.data):
                raise validators.ValidationError("Invalid password")

    def get_user(self, session):
        return session.query(Account).filter_by(login=self.login.data).first()
