from telebot import types

from tbot import get_bot
from tbot.core.questionnaire import Questionnaire
from tbot.utils import save_user, get_user_if_exist
from tbot.datatypes import User, House


bot = get_bot()
def success_callback(): pass


class HouseQuestionnaire(Questionnaire):
    class Meta:
        model = House
        fields = ("number", "street", "area",)


class UserQuestionnaire(Questionnaire):
    house = HouseQuestionnaire

    class Meta:
        model = User
        fields = ("name", "phone", "house", "flat")


def get_entry(success_callback_):
    global success_callback
    success_callback = success_callback_

    return entry


def entry(message, house: House):
    chat_id = message.chat.id
    user, exist = get_user_if_exist(chat_id)

    is_empty = False
    if not exist:
        user = User(id=chat_id)
        is_empty = True

    if house is None:
        user.house = House()
        is_model_fields_empty = True
    else:
        user.house = house
        is_model_fields_empty = False

    questionnaire = UserQuestionnaire(
        chat_id, user, next_step_handler=save_user_handler,
        is_empty=is_empty,
        is_model_fields_empty=is_model_fields_empty
    )
    questionnaire.run()


def save_user_handler(user):
    chat_id = user.id
    markup = types.ReplyKeyboardRemove()
    bot.send_message(chat_id, "OK. Lets register you", reply_markup=markup)
    save_user(user)
    success_callback(chat_id)
