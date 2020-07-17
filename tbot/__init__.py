import telebot
from config import config

bot = telebot.TeleBot(config.get("telegram", "token"))


def get_bot():
    return bot
