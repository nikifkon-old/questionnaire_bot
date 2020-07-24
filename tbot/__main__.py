import logging

from aiogram import executor
from aiogram.utils.executor import start_webhook

from config import Config
from tbot.bot import dp, bot

logging.basicConfig(level=logging.INFO)


async def on_startup(app):
    """Simple hook for aiohttp application which manages webhook"""
    await bot.delete_webhook()
    await bot.set_webhook(Config.WEBHOOK_URL)


async def on_shutdown(dp):
    logging.warning('Shutting down..')

    # insert code here to run it before shutdown

    # Remove webhook (not acceptable in some cases)
    await bot.delete_webhook()

    # Close DB connection (if used)
    await dp.storage.close()
    await dp.storage.wait_closed()

    logging.warning('Bye!')


if __name__ == '__main__':
    if Config.USE_POLLING:
        executor.start_polling(dp, skip_updates=True)
    else:
        start_webhook(
            dispatcher=dp,
            webhook_path=Config.WEBHOOK_PATH,
            on_startup=on_startup,
            on_shutdown=on_shutdown,
            skip_updates=True,
            host=Config.WEBAPP_HOST,
            port=Config.WEBAPP_PORT,
        )
