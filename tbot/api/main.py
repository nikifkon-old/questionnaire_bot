from flask import Flask
from flask_admin import Admin

from config import Config
from tbot import listeners  # noqa
from tbot import models
from tbot.db import Session
from tbot.api import routes
from tbot.api.admin import init_login
from tbot.api.admin.views import (
    MyAdminIndexView, UserView, HouseView, EventView, AccountView, AreaView
)

app = Flask(__name__)
app.config["SECRET_KEY"] = Config.SECRET_KEY
app.config["JSON_AS_ASCII"] = False

app.register_blueprint(routes.event_api)
app.register_blueprint(routes.house_api)
app.register_blueprint(routes.event_api)
app.register_blueprint(routes.index_page)


# Initialize flask-login
init_login(app)


admin = Admin(app, index_view=MyAdminIndexView(),
              base_template='my_master.html')
admin.add_view(AccountView(models.Account, Session()))
admin.add_view(EventView(models.Event, Session()))
admin.add_view(HouseView(models.House, Session()))
admin.add_view(AreaView(models.Area, Session()))
admin.add_view(UserView(models.User, Session()))
