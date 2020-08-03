from aiogram import types

from tbot import messages, schemas
from tbot.bot import bot, i18n, storage
from tbot.utils import update_user


async def bot_exitupdate(message: types.Message):
    """
    /exitupdate command handler in `updating` state
    """
    user_id = message.from_user.id
    data = await storage.get_data(user=user_id)
    user_json = data["user"]
    user = schemas.User(**user_json)
    update_user(user)

    i18n.ctx_locale.set(user.lang)

    await storage.reset_state(user=user_id)
    await storage.reset_data(user=user_id)

    await bot.send_message(
        chat_id=user_id,
        text=messages.CMD_EXITUPDATE_MESSAGE.format(user_data=user)
    )
