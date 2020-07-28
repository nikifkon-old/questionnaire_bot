import flask_admin as admin
import flask_login as login
from flask import redirect, request, url_for
from flask_admin import expose, helpers
from flask_admin.contrib import sqla
from pydantic import ValidationError as PydanticValidationError
from wtforms import PasswordField, TextAreaField
from wtforms.validators import ValidationError

from tbot import models, schemas
from tbot.utils import session_scope

from .forms import LoginForm


# Create customized model view class
class MyModelView(sqla.ModelView):
    def is_accessible(self):
        return login.current_user.is_authenticated


# Create customized index view class that handles login & registration
class MyAdminIndexView(admin.AdminIndexView):
    @expose("/")
    def index(self):
        if not login.current_user.is_authenticated:
            return redirect(url_for(".login_view"))
        return super(MyAdminIndexView, self).index()

    @expose("/login/", methods=("GET", "POST"))
    def login_view(self):
        # handle user login
        with session_scope() as session:
            form = LoginForm(request.form)
            if helpers.validate_form_on_submit(form):
                user = form.get_user(session)
                login.login_user(user)

            if login.current_user.is_authenticated:
                return redirect(url_for(".index"))
            self._template_args["form"] = form
            return super(MyAdminIndexView, self).index()

    @expose("/logout/")
    def logout_view(self):
        login.logout_user()
        return redirect(url_for(".index"))


class UserView(MyModelView):
    pass


class HouseView(MyModelView):
    form_excluded_columns = ("events", "users",)


class AccountView(MyModelView):
    column_exclude_list = ("password",)
    form_excluded_columns = ("password",)
    form_extra_fields = {
        "new_password": PasswordField("New password")
    }

    def on_model_change(self, form, account: models.Account, is_created):
        new_password = form.new_password.data
        if new_password is not None:
            if len(new_password) < 4:
                raise ValidationError("Password is too short. It must be at least 5 characters")
            if not is_created and account.check_password(new_password):
                raise ValidationError("This password is already in use")
            account.set_password(new_password)
        return account


class AreaView(MyModelView):
    form_excluded_columns = ("houses", "events")


EMERGENCY = schemas.EventType.EMERGENCY
SCHEDUELD_WORK = schemas.EventType.SCHEDUELD_WORK
UNSCHEDUELD_WORK = schemas.EventType.UNSCHEDUELD_WORK

ALL = schemas.EventTarget.ALL
HOUSE = schemas.EventTarget.HOUSE
AREA = schemas.EventTarget.AREA


class EventView(MyModelView):
    form_overrides = {
        "description": TextAreaField
    }
    form_excluded_columns = ("messages",)
    column_exclude_list = ("description",)

    form_choices = {
        "type": [
            (EMERGENCY.value, EMERGENCY.value),
            (SCHEDUELD_WORK.value, SCHEDUELD_WORK.value),
            (UNSCHEDUELD_WORK.value, UNSCHEDUELD_WORK.value),
        ],
        "target": [
            (ALL.value, ALL.value),
            (HOUSE.value, HOUSE.value),
            (AREA.value, AREA.value),
        ]
    }

    def on_model_change(self, form, model, is_created):
        data = form.data
        if data["area"]:
            data["area"] = schemas.Area.from_orm(data["area"])
        if data["house"]:
            data["house"] = schemas.House.from_orm(data["house"])
        try:
            if is_created:
                schemas.EventCreate(**data)
            else:
                data["id"] = model.id
                schemas.EventUpdate(**data)
        except PydanticValidationError as exc:
            error = exc.errors()[0]
            msg = "Error in '{loc[0]}': {msg}".format(**error)
            raise ValidationError(msg)
        return model
