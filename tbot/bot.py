import asyncio
from pathlib import Path

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage
from aiogram.types import ParseMode

from config import Config
from tbot.middleware import I18nMiddleware

# For flask sessions
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()

I18N_DOMAIN = "tbot"
BASE_DIR = Path(__file__).parent.parent
LOCALES_DIR = BASE_DIR / "locales"

bot = Bot(token=Config.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML, loop=loop)
storage = RedisStorage(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    loop=loop
)
dp = Dispatcher(bot, storage=storage)

i18n = I18nMiddleware(I18N_DOMAIN, LOCALES_DIR)
dp.middleware.setup(i18n)
