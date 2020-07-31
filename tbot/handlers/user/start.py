from aiogram import types

from tbot import messages, schemas
from tbot.bot import bot
from tbot.handlers.utils import process_if_user_exit, send_welcome_message
from tbot.utils import save_user

from .register import bot_register


async def bot_start(message: types.Message):
    """
    /start command handler
    """
    chat_id = message.chat.id
    continue_ = await process_if_user_exit(user_id=chat_id)
    if continue_:
        payload = message.get_args()
        if payload:
            data, created = schemas.House.from_string(payload)
            if created:
                user_lang = message.from_user.language_code
                user = schemas.User(id=chat_id, house=data, lang=user_lang)
                save_user(user)
                await send_welcome_message(user)
            else:
                await bot.send_message(
                    chat_id=chat_id,
                    text=messages.INVALID_START_PAYLOAD_ERROR.format(error_message=data["error_msg"])
                )
        else:
            await bot.send_message(
                chat_id=chat_id,
                text=messages.START_MESSAGE
            )
            await bot_register(message)
