import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.types import ParseMode

from config import Config

# For flask sessions
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()

bot = Bot(token=Config.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML, loop=loop)
storage = RedisStorage(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    loop=loop
)
dp = Dispatcher(bot, storage=storage)
