import re

import aiogram.utils.markdown as md
from aiogram import executor, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ParseMode

from tbot import get_bot, get_dp
from tbot import schemas
from tbot.utils import get_user, save_user, update_user


bot = get_bot()
dp = get_dp()


class ShortForm(StatesGroup):
    area = State()
    street = State()
    number = State()


# FIXME: this state group contain only one state, and one 'storage-state', may use storage straight
class FullForm(StatesGroup):
    get_next_field = State()
    user = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message):
    continue_ = await process_if_user_exit(user_id=message.chat.id)
    if continue_:
        payload_patter = re.compile(r"/start (?P<payload>.*)")
        match = re.match(payload_patter, message.text)
        if match is None:
            await cmd_register(message)
        else:
            payload = match.group("payload")

            # register user
            house = schemas.House.from_string(payload)
            user = schemas.User(id=message.chat.id, house=house)
            save_user(user)
            await send_welcome_message(user)


@dp.message_handler(commands=["register"])
async def cmd_register(message: types.Message):
    """
    User registresion entry point
    """
    continue_ = await process_if_user_exit(user_id=message.chat.id)
    if continue_:
        await ShortForm.area.set()

        await message.reply("Enter your area")


async def process_if_user_exit(user_id: int) -> bool:
    user = get_user(user_id)
    if user is None:
        return True
    else:
        await bot.send_message(
            chat_id=user_id,
            text=md.text(
                "You are already registered.",
                "Your account data is:",
                md.italic(str(user)),
                "If you would like to update or full it. Go to /update.",
                sep="\n"
            ),
            parse_mode=ParseMode.MARKDOWN
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
        text=md.text(
            "All right! Your now registed",
            "Your account data is",
            md.text("House", md.bold(str(user.house))),
            sep="\n"
        ),
        parse_mode=ParseMode.MARKDOWN
    )


@dp.message_handler(commands=["update"])
async def cmd_update(message: types.Message):
    chat_id = message.chat.id
    user = get_user(chat_id)
    await bot.send_message(
        chat_id=chat_id,
        text=md.text(
            "Your account data is: ",
            md.italic(str(user)),
            md.text("Please provide field you wanna update or type",
                    md.bold("exit")),
            sep="\n"
        ),
        parse_mode=ParseMode.MARKDOWN
    )
    await FullForm.get_next_field.set()


@dp.message_handler(state=FullForm.get_next_field)
async def process_next_field(message: types.Message, state: FSMContext):
    chat_id = message.chat.id

    data = state.get_data()

    # FIXME: this code should be in cmd_update, but I dont known how access state in entry point
    if data.get("user") is None:
        state.update_data(user=get_user(chat_id))

    if message.text == "exit":
        update_user(data["user"])

        await state.finish()
        await bot.send_message(
            chat_id=chat_id,
            text=md.text(
                "Every this is ok",
                "Now. Your account data is: ",
                md.italic(str(data["user"])),
                sep="\n"
            ),
            parse_mode=ParseMode.MARKDOWN
        )
    else:
        payload = message.text.split(", ", maxsplit=1)
        if len(payload) == 2:
            # FIXME: this should be in schema models
            user_keys = set(schemas.User.schema()[
                            "properties"].keys()) - {"id", "house"}
            house_keys = set(schemas.House.schema()[
                "properties"].keys()) - {"id"}

            async with state.proxy() as data:
                if payload[0] in user_keys:
                    setattr(data["user"], payload[0], payload[1])
                elif payload[0] in house_keys:
                    setattr(data["user"].house, payload[0], payload[1])

                await bot.send_message(
                    chat_id=chat_id,
                    text=md.text(
                        "Your account data is: ",
                        md.italic(str(data["user"])),
                        md.text("Please provide field you wanna update or type",
                                md.bold("exit")),
                        sep="\n"
                    ),
                    parse_mode=ParseMode.MARKDOWN
                )
                await FullForm.get_next_field.set()

        else:
            await bot.send_message(
                chat_id=chat_id,
                text=md.text(
                    "Invalid format or doesnt exist field",
                    sep="\n"
                ),
                parse_mode=ParseMode.MARKDOWN
            )
            await FullForm.get_next_field.set()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
