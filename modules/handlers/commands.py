from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from modules.services.database import FavoritesRedis
import modules.messageTemplates as template
from modules.types.markup import MainMenuMarkup

import config


async def start(message: types.Message, state: FSMContext, db: FavoritesRedis):
    """
    Function called on `/start` command

    Creates new user instance in the database and sends welcome message

    Resets the state
    """

    try:
        db.new_user(message.from_user.id)
        await message.answer(text=template.START, reply_markup=MainMenuMarkup())
        await state.set_state(None)
    except Exception as e:
        await message.answer(template.START_DB_ERROR)


async def help_msg(message: types.Message):
    await message.answer(template.HELP)


def setup(dp: Dispatcher):
    dp.message.register(start, Command("start"))

    dp.message.register(help_msg, Command("help"))
    dp.message.register(help_msg, F.text == template.BUTTON_HELP)
