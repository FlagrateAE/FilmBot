from aiogram import Dispatcher, types
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import StateMachine
from modules.types.markup import MainMenuMarkup


async def start(message: types.Message, state: FSMContext, db: FavoritesDB):
    """
    Function called on `/start` command

    Creates new user instance in the database and sends welcome message

    Sets `StateMachine.main_menu` state
    """

    try:
        db.new_user(message.from_user.id)
        await message.answer(text=Template.START, reply_markup=MainMenuMarkup())
        await state.set_state(StateMachine.main_menu)
    except Exception as e:
        await message.answer(Template.START_DB_ERROR)


async def get_all_data(message: types.Message, db: FavoritesDB):
    """
    Used for db testing and output. Will be removed in prod or kept for admins

    Sends back all the data in the database
    """

    await message.answer(str(db.get_all()))


def setup(dp: Dispatcher):
    dp.message.register(start, Command("start"))

    dp.message.register(get_all_data, Command("all"))
