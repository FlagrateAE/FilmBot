from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import StateMachine
from modules.types.markup import FavoritesClearMarkup, MainMenuMarkup


async def search_start(message: types.Message, state: FSMContext):
    await message.answer(Template.FSM_SEARCH_START)
    await state.set_state(StateMachine.search_input)


async def clear_confirm(message: types.Message, state: FSMContext, db: FavoritesDB):
    if db.get_user_movies(message.from_user.id):
        await message.answer(
            text=Template.CLEAR_CONFIRM, reply_markup=FavoritesClearMarkup()
        )
        await state.set_state(StateMachine.clear_confirm)
    else:
        # no favorites to clear
        await message.answer(Template.FAVORITES_EMPTY)


async def clear_yes(message: types.Message, state: FSMContext, db: FavoritesDB):
    db.clear_user_movies(message.from_user.id)
    await message.answer(text=Template.CLEAR_FINISHED, reply_markup=MainMenuMarkup())
    await state.set_state(StateMachine.main_menu)


async def clear_no(message: types.Message, state: FSMContext):
    await message.answer(text=Template.CLEAR_CANCELLED, reply_markup=MainMenuMarkup())
    await state.set_state(StateMachine.main_menu)


def setup(dp: Dispatcher):
    dp.message.register(
        search_start, F.text == Template.SEARCH_BUTTON, StateMachine.main_menu
    )

    dp.message.register(
        clear_confirm, F.text == Template.FAVORITES_CLEAR_BUTTON, StateMachine.main_menu
    )
    dp.message.register(
        clear_confirm, Command("clear_favorites"), StateMachine.main_menu
    )

    dp.message.register(
        clear_yes, F.text == Template.CLEAR_YES_BUTTON, StateMachine.clear_confirm
    )
    dp.message.register(
        clear_no, F.text == Template.CLEAR_NO_BUTTON, StateMachine.clear_confirm
    )
