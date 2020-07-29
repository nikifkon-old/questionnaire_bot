from aiogram import Dispatcher

from tbot.states import user as user_states

from .delete_account import bot_delete_account
from .exitupdate import bot_exitupdate
from .register import bot_register
from .start import bot_start
from .update import bot_update, process_updating


def setup(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands=["start"])
    dp.register_message_handler(bot_register, commands=["register"])
    dp.register_message_handler(bot_update, commands=["update"])
    dp.register_message_handler(bot_delete_account, commands=["delete_account"])
    dp.register_message_handler(bot_exitupdate, state=user_states.UPDATING_STATE, commands=["exitupdate"])
    dp.register_message_handler(process_updating, state=user_states.UPDATING_STATE)
