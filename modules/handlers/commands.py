from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import SpecialStateMachine
from modules.types.markup import MainMenuMarkup

import config


async def start(message: types.Message, state: FSMContext, db: FavoritesDB):
    """
    Function called on `/start` command

    Creates new user instance in the database and sends welcome message

    Resets the state
    """

    try:
        db.new_user(message.from_user.id)
        await message.answer(text=Template.START, reply_markup=MainMenuMarkup())
        await state.set_state(None)
    except Exception as e:
        await message.answer(Template.START_DB_ERROR)


async def help_msg(message: types.Message):
    await message.answer(Template.HELP)


async def get_all_data(message: types.Message, db: FavoritesDB):
    """
    Used for db testing and output. Will be removed in prod or kept for admins

    Sends back all the data in the database
    """
    if not message.from_user.id in config.ADMINS:
        await message.answer(Template.ACCESS_DENIED)
    else:
        await message.answer(str(db.get_all()))


def setup(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    
    dp.message.register(help_msg, Command("help"))
    dp.message.register(help_msg, F.text == Template.HELP_BUTTON)
    
    dp.message.register(get_all_data, Command("all"))
