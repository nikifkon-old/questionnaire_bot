from aiogram import types

from tbot import messages, schemas
from tbot.bot import bot, dp, i18n, storage
from tbot.handlers.utils import update_user_by_text
from tbot.states import user as user_states
from tbot.utils import get_user

_ = i18n.gettext


async def bot_update(message: types.Message):
    """
    /update command handler
    """
    chat_id = message.chat.id
    user = get_user(chat_id)

    if user is not None:
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(user_states.UPDATING_STATE)
        await storage.set_data(user=message.from_user.id, data={"user": user.dict()})

        await bot.send_message(
            chat_id=chat_id,
            text=_(messages.CMD_UPDATE).format(user_data=user),
        )
    else:
        await bot.send_message(
            chat_id=chat_id,
            text=_(messages.YOU_ARE_NOT_REGISTERED_ERROR)
        )


async def process_updating(message: types.Message):
    """
    Process update operation
    """
    user_id = message.from_user.id
    data = await storage.get_data(chat=user_id)
    user_json = data.get("user")
    user = schemas.User(**user_json)
    data, updated = update_user_by_text(user, message.text)
    if updated:
        user_dict = data["user"].dict()
        await storage.set_data(user=user_id, data={"user": user_dict})

        await bot.send_message(
            chat_id=user_id,
            text=_(messages.UPDATE_ITERATION_SUCCESS).format(field=data["field"])
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text=_(messages.UPDATE_ITERATION_FAILED).format(error_message=data["error_msg"])
        )
