from tbot import messages, schemas
from tbot.bot import bot
from tbot.utils import deep_setter, get_user


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
            text=messages.YOU_ARE_ALREADY_REGISTERED_MESSAGE.format(user_data=str(user))
        )
        return False
    await send_welcome_message(user)


async def send_welcome_message(user: schemas.User):
    await bot.send_message(
        chat_id=user.id,
        text=messages.WELCOME_MESSAGE.format(user_data=user)
    )


def update_user_by_text(text: str, user):
    """
    Update user by message text format like {user_alias}, {new_value}
    """
    # TODO: return updated user
    if ", " in text:
        key, value = text.split(", ")
    else:
        return False, {
            "error_msg": messages.SEPERETE_BY_COMMA_ERROR
        }

    if key in schemas.user_aliases:
        alias = schemas.user_aliases[key]
        deep_setter(user, alias, value)
        return True, {"field": key}

    else:
        return False, {
            "error_msg": messages.NOT_VALID_FIELD_ERROR.format(
                field=key,
                fields=schemas.get_valid_user_fields()
            )
        }
