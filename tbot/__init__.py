import telebot
from config import config

bot = telebot.TeleBot(config["DEFAULT"]["token"])


def get_bot():
    return bot
