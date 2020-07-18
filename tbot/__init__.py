from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config import Config


bot = Bot(token=Config.TELEGRAM_TOKEN)
storage = MemoryStorage()  # FIXME: use memory storage
dp = Dispatcher(bot, storage=storage)


def get_bot():
    return bot


def get_dp():
    return dp
