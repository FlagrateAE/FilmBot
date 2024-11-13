from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext

from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import SpecialStateMachine
from modules.types.markup import FavoritesClearMarkup, MainMenuMarkup


async def search_start(message: types.Message, state: FSMContext):
    """
    Called on search button pressed in main menu.
    Starts a search process

    Sets `StateMachine.search_input` state
    """

    await message.answer(Template.FSM_SEARCH_START)
    await state.set_state(SpecialStateMachine.search_input)


async def clear_confirm(message: types.Message, state: FSMContext, db: FavoritesDB):
    """
    Called on clear button pressed in main menu.
    Start a clear confirmation dialog

    Sets `StateMachine.clear_confirm` state
    """

    if db.get_user_movies(message.from_user.id):
        await message.answer(
            text=Template.CLEAR_CONFIRM, reply_markup=FavoritesClearMarkup()
        )
        await state.set_state(SpecialStateMachine.clear_confirm)
    else:
        # no favorites to clear
        await message.answer(Template.FAVORITES_EMPTY)


async def clear_yes(message: types.Message, state: FSMContext, db: FavoritesDB):
    """
    Called on clear confiramtion by respective keyboard button. Clears user favorite movies list.

    Resets the state
    """

    db.clear_user_movies(message.from_user.id)
    await message.answer(text=Template.CLEAR_FINISHED, reply_markup=MainMenuMarkup())
    await state.set_state(None)


async def clear_no(message: types.Message, state: FSMContext):
    """
    Called on clear refusal by respective keyboard button. Sends back to main menu.

    Resets the state
    """

    await message.answer(text=Template.CLEAR_CANCELLED, reply_markup=MainMenuMarkup())
    await state.set_state(None)


def setup(dp: Dispatcher):
    dp.message.register(search_start, F.text == Template.SEARCH_BUTTON)

    dp.message.register(clear_confirm, F.text == Template.FAVORITES_CLEAR_BUTTON)
    dp.message.register(clear_confirm, Command("clear_favorites"))

    dp.message.register(
        clear_yes,
        F.text == Template.CLEAR_YES_BUTTON,
        SpecialStateMachine.clear_confirm,
    )
    dp.message.register(
        clear_no, F.text == Template.CLEAR_NO_BUTTON, SpecialStateMachine.clear_confirm
    )
