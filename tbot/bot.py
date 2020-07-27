import asyncio

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from tbot import schemas
from tbot.utils import deep_setter, get_user, save_user, update_user
from tbot import messages
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage

from config import Config

# For flask sessions
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()

bot = Bot(token=Config.TELEGRAM_TOKEN, parse_mode=ParseMode.HTML, loop=loop)
storage = RedisStorage(
    host=Config.REDIS_HOST,
    port=Config.REDIS_PORT,
    password=Config.REDIS_PASSWORD,
    loop=loop
)
dp = Dispatcher(bot, storage=storage)


class ShortForm(StatesGroup):
    area = State()
    street = State()
    number = State()


UPDATING_STATE = "updating"


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
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
            await cmd_register(message)


@dp.message_handler(commands=["register"])
async def cmd_register(message: types.Message):
    """
    User registresion entry point
    /register command handler
    """
    continue_ = await process_if_user_exit(user_id=message.chat.id)
    if continue_:
        await ShortForm.area.set()

        await message.reply("Enter your area")


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


@dp.message_handler(state=ShortForm.area)
async def process_area(message: types.Message, state: FSMContext):
    """
    Process user's area
    """
    await state.update_data(area=message.text)

    await ShortForm.next()
    await message.reply("Enter your street")


@dp.message_handler(state=ShortForm.street)
async def process_street(message: types.Message, state: FSMContext):
    """
    Process user's street
    """
    await state.update_data(street=message.text)

    await ShortForm.next()
    await message.reply("Enter your house number")


@dp.message_handler(lambda message: not message.text.isdigit(), state=ShortForm.number)
async def process_number_ivalid(message: types.Message, state: FSMContext):
    """
    Process invalid user's house number
    """
    await message.reply("Opps... house number must contain only digits. Please try again")


@dp.message_handler(state=ShortForm.number)
async def process_number(message: types.Message, state: FSMContext):
    """
    Process user's house number
    """
    await state.update_data(number=int(message.text))

    data = await state.get_data()
    await state.finish()

    # register user
    user = schemas.User(id=message.chat.id, house=data)
    save_user(user)

    await send_welcome_message(user)


async def send_welcome_message(user: schemas.User):
    await bot.send_message(
        chat_id=user.id,
        text=messages.WELCOME_MESSAGE.format(user_data=user)
    )


@dp.message_handler(commands=["update"])
async def cmd_update(message: types.Message):
    """
    /update command handler
    """
    chat_id = message.chat.id
    user = get_user(chat_id)

    if user is not None:
        state = dp.current_state(user=message.from_user.id)
        await state.set_state(UPDATING_STATE)
        await storage.set_data(user=message.from_user.id, data={"user": user.dict()})

        await bot.send_message(
            chat_id=chat_id,
            text=messages.CMD_UPDATE.format(user_data=user),
        )
    else:
        pass  # TODO


@dp.message_handler(state=UPDATING_STATE, commands=["exitupdate"])
async def cmd_exitupdate(message: types.Message):
    """
    /exitupdate command handler in `updating` state
    """
    user_id = message.from_user.id
    data = await storage.get_data(user=user_id)
    user_json = data["user"]
    user = schemas.User(**user_json)
    update_user(user)
    await bot.send_message(
        chat_id=user_id,
        text=messages.CMD_EXITUPDATE.format(user_data=user)
    )
    await storage.reset_state(user=user_id)
    await storage.reset_data(user=user_id)


@dp.message_handler(state=UPDATING_STATE)
async def process_updating(message: types.Message):
    """
    Process update operation
    """
    user_id = message.from_user.id
    data = await storage.get_data(chat=user_id)
    user_json = data.get("user")
    user = schemas.User(**user_json)
    updated, data = update(text=message.text, user=user)
    if updated:
        await storage.set_data(user=user_id, data={"user": user.dict()})

        await bot.send_message(
            chat_id=user_id,
            text=messages.UPDATE_ITERATION_SUCCESS.format(field=data["field"])
        )
    else:
        await bot.send_message(
            chat_id=user_id,
            text=messages.UPDATE_ITERATION_FAILED.format(error_message=data["error_msg"])
        )


def update(text: str, user):
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
