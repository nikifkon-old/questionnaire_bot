from copy import deepcopy
from typing import Tuple

from tbot import messages, schemas
from tbot.bot import bot, i18n
from tbot.utils import deep_setter, get_user

_ = i18n.gettext


async def process_if_user_exit(user_id: int) -> bool:
    """
    Check if user already exit, and send message about it
    """
    user = get_user(user_id)
    if user is None:
        return True
    else:
        await bot.send_message(
            chat_id=user_id,
            text=_(messages.YOU_ARE_ALREADY_REGISTERED_MESSAGE).format(user_data=str(user))
        )
        return False
    await send_welcome_message(user)


async def send_welcome_message(user: schemas.User):
    await bot.send_message(
        chat_id=user.id,
        text=_(messages.WELCOME_MESSAGE).format(user_data=user)
    )


def update_user_by_text(user: schemas.User, text: str) -> Tuple[dict, bool]:
    """
    Update user by message text format like {user_alias}, {new_value}

    :param user: The user you wanna update
    :param text: Message text
    :returns: A tuple with `result` data and `state`

    If updated was successfully:
        state is `True`
        result is
        {
            "user": :obj:`schemas.User`,
            "field": `str`
        }
    else:
        state is `False`
        result is
        {
            "error_msg": `str`
        }


    """
    if ", " in text:
        key, value = text.split(", ")
    else:
        return {
            "error_msg": _(messages.SEPERETE_BY_COMMA_ERROR)
        }, False

    if key in schemas.user_aliases:
        alias = schemas.user_aliases[key]
        new_user = deepcopy(user)
        deep_setter(new_user, alias, value)
        return {"field": key, "user": new_user}, True

    else:
        return {
            "error_msg": _(messages.NOT_VALID_FIELD_ERROR).format(
                field=key,
                fields=schemas.get_valid_user_fields()
            )
        }, False
