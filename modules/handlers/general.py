from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import StateMachine, Movie
from modules.types.markup import (
    InfoInlineMarkup,
    SearchResultInlineMarkup,
    FavoritesInlineMarkup,
)


async def _send_movie(
    message: types.Message, movie: Movie, markup: types.InlineKeyboardMarkup
):
    """
    Internal function for sending movie info to the user in a form of message

    Parameters
    ----------
    message : types.Message
        The message object as a pointer to chat
    movie : Movie
        The movie object to send.
    markup : types.InlineKeyboardMarkup
        The inline keyboard markup to attach to the message.
    """

    if movie.poster_path:
        await message.answer_photo(
            photo=movie.poster_path,
            caption=movie.text,
            reply_markup=markup,
        )
    else:
        await message.answer(text=movie.text, reply_markup=markup)


async def search(
    message: types.Message,
    state: FSMContext,
    movie_api: MovieAPI,
    db: FavoritesDB,
    command: CommandObject = None,
):
    """
    Called on `/search` command or on user input in `StateMachine.search_input` state.
    Searches using movie title and sends the best match to the user. Writes other results (if any) to state data

    Sets `StateMachine.main_menu` state
    """

    if command:
        if command.args:
            query = command.args
        else:
            await message.answer(Template.SEARCH_NO_ARGS)
    else:
        query = message.text

    results = movie_api.search(query)

    if not results:
        await message.answer(Template.SEARCH_NOT_FOUND)
        return

    best_result = results[0]

    action = (
        "add"
        if best_result.movie_id not in db.get_user_movies(message.from_user.id)
        else "remove"
    )

    if len(results) > 1:
        markup = SearchResultInlineMarkup(
            movie_id=best_result.movie_id, favorites_action=action
        )
    else:
        markup = InfoInlineMarkup(
            movie_id=best_result.movie_id, favorites_action=action
        )

    await _send_movie(message, best_result, markup)

    await state.set_state(StateMachine.main_menu)
    if len(results) > 1:
        await state.set_data({"other_results": results[1:]})


async def list_favorites(message: types.Message, movie_api: MovieAPI, db: FavoritesDB):
    """
    Called on `/favorites` command or on button "Show favorites" in main menu.

    Sends the user a list of all their favorites in a form of inline buttons
    """

    favorites = db.get_user_movies(message.from_user.id)

    if not favorites:
        await message.answer(Template.FAVORITES_EMPTY)
        return

    markup = FavoritesInlineMarkup(movie_api.movie_factory(favorites))
    await message.answer(text=Template.FAVORITES_SHOW_BUTTON, reply_markup=markup)


def setup(dp: Dispatcher):
    dp.message.register(search, Command("search"))
    dp.message.register(search, F.text, StateMachine.search_input)

    dp.message.register(list_favorites, Command("favorites"))
    dp.message.register(
        list_favorites, F.text == Template.FAVORITES_SHOW_BUTTON, StateMachine.main_menu
    )
