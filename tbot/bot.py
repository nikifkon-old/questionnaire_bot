import logging

from transliterate import translit

from tbot import get_bot, registeration
from tbot import schemas
from tbot.listeners import event_handler  # noqa


logger = logging.getLogger(__file__)
bot = get_bot()


@bot.message_handler(commands=["start"])
def start_handler(message):
    house = None
    if " " in message.text:
        payload = message.text.split("/start ")[1]
        house = schemas.House.from_string(translit(payload, 'ru'))
    bot.send_message(message.chat.id,
                     "Hello. Answer a few questions to start using this bot")
    registeration.get_entry(auth_successed)(message, house=house)


@bot.message_handler(commands=["auth"])
def auth_handler(message):
    registeration.get_entry(auth_successed)(message, house=None)


def auth_successed(chat_id):
    bot.send_message(chat_id, "All Fine!")


if __name__ == "__main__":
    bot.polling()
