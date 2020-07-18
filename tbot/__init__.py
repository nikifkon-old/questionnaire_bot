import telebot
from config import Config

bot = telebot.TeleBot(Config.TELEGRAM_TOKEN)


def get_bot():
    return bot
