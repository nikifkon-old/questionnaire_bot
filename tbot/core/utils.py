from telebot import types


def get_yes_or_no_keyboard():
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    yes_btn = types.KeyboardButton("Yes")
    no_btn = types.KeyboardButton("No")
    keyboard.add(yes_btn, no_btn)
    return keyboard
