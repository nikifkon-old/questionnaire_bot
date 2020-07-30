from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup

from tbot import messages, schemas
from tbot.bot import dp, i18n
from tbot.handlers.utils import process_if_user_exit, send_welcome_message
from tbot.utils import save_user

_ = i18n.gettext


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

        await message.reply(_(messages.ASK_AREA_MESSAGE))


@dp.message_handler(state=ShortForm.area)
async def process_area(message: types.Message, state: FSMContext):
    """
    Process user's area
    """
    await state.update_data(area=message.text)

    await ShortForm.next()
    await message.reply(_(messages.ASK_STREET_MESSAGE))


@dp.message_handler(state=ShortForm.street)
async def process_street(message: types.Message, state: FSMContext):
    """
    Process user's street
    """
    await state.update_data(street=message.text)

    await ShortForm.next()
    await message.reply(_(messages.ASK_HOUSE_NUMBER_MESSAGE))


@dp.message_handler(lambda message: not message.text.isdigit(), state=ShortForm.number)
async def process_number_ivalid(message: types.Message, state: FSMContext):
    """
    Process invalid user's house number
    """
    await message.reply(_(messages.NOT_DIGITAL_NUMBER_ERROR))


@dp.message_handler(state=ShortForm.number)
async def process_number(message: types.Message, state: FSMContext):
    """
    Process user's house number
    """
    await state.update_data(number=int(message.text))

    data = await state.get_data()
    await state.finish()

    # register user
    user_lang = message.from_user.language_code
    user = schemas.User(id=message.chat.id, house=data, lang=user_lang)
    save_user(user)
    await send_welcome_message(user)
