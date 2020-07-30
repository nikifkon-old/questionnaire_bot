from aiogram import types

from tbot import messages
from tbot.bot import bot, i18n
from tbot.utils import delete_user_by_id

_ = i18n.gettext


async def bot_delete_account(message: types.Message):
    """
    /delete_account command handler
    """
    chat_id = message.chat.id
    deleted = delete_user_by_id(chat_id)
    if deleted:
        await bot.send_message(
            chat_id=chat_id,
            text=_(messages.DELETED_ACCOUNT_SUCCESSFULLY)
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=_(messages.YOU_ARE_NOT_REGISTERED_ERROR).format(action="delete your account")
        )
