from tbot.database import DB
from tbot.datatypes import User
from config import config


def get_db():
    return DB(config["database"]["sqlite_file_path"])


def save_user(user: User):
    get_db().save_user(user)


def get_user_if_exist(chat_id: int):
    return get_db().get_user_if_exist(chat_id)
