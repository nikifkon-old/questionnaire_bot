from aiogram import types

from .register import bot_register
from tbot import schemas
from tbot.utils import save_user
from tbot.handlers.utils import process_if_user_exit, send_welcome_message


async def bot_start(message: types.Message):
    """
    /start command handler
    """
    continue_ = await process_if_user_exit(user_id=message.chat.id)
    if continue_:
        payload = message.get_args()
        if payload:
            # TODO ivalid format
            house = schemas.House.from_string(payload)
            user = schemas.User(id=message.chat.id, house=house)
            save_user(user)
            await send_welcome_message(user)
        else:
            await bot_register(message)
