from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from tbot import schemas
from tbot.bot import dp
from tbot.handlers.utils import process_if_user_exit, send_welcome_message
from tbot.utils import save_user


class ShortForm(StatesGroup):
    area = State()
    street = State()
    number = State()


async def bot_register(message: types.Message):
    """
    User registresion entry point
    /register command handler
    """
    continue_ = await process_if_user_exit(user_id=message.chat.id)
    if continue_:
        await ShortForm.area.set()

        await message.reply("Enter your area")


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
