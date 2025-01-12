from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.utils.media_group import MediaGroupBuilder

from modules.services.movieAPI import MovieAPI
from modules.services.database import FavoritesRedis
from modules.types.common import MessageTemplates as template
from modules.types.common import SpecialStateMachine, Movie
from modules.types.markup import (
    InfoInlineMarkup,
    SearchResultInlineMarkup,
    FavoritesInlineMarkup,
    TrendingInlineMarkup,
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


async def _handle_command_search(
    message: types.Message, command: CommandObject
) -> str | None:
    """Handle search from command with arguments"""
    if not command.args:
        await message.answer(template().SEARCH_MISSING_QUERY)
        return None
    return command.args


async def _handle_message_search(message: types.Message, command=None) -> str:
    """Handle search from direct message"""
    return message.text


async def search(
    message: types.Message,
    state: FSMContext,
    movie_api: MovieAPI,
    db: FavoritesRedis,
    command: CommandObject = None,
):
    """
    Called on `/search` command or on user input in `StateMachine.search_input` state.
    Searches using movie title and sends the best match to the user. Writes other results (if any) to state data

    Resets the state
    """

    search_handlers = {True: _handle_command_search, False: _handle_message_search}

    query = await search_handlers[command is not None](message, command)
    if not query:
        return

    results = movie_api.search(query)

    if not results:
        await message.answer(template().SEARCH_NOT_FOUND)
        return

    best_result = results[0]

    action = (
        "add"
        if best_result.movie_id not in db.get_user_movies(message.from_user.id)
        else "remove"
    )

    if len(results) > 1:
        other_ids = [result.movie_id for result in results[1:]]

        markup = SearchResultInlineMarkup(
            movie_id=best_result.movie_id,
            favorites_action=action,
            other_results_ids=other_ids,
        )
    else:
        markup = InfoInlineMarkup(
            movie_id=best_result.movie_id, favorites_action=action
        )

    await _send_movie(message, best_result, markup)

    await state.set_state(None)
    if len(results) > 1:
        await state.set_data({"other_results": results[1:]})


async def list_favorites(
    message: types.Message, movie_api: MovieAPI, db: FavoritesRedis
):
    """
    Called on `/favorites` command or on button "Show favorites" in main menu.

    Sends the user a list of all their favorites in a form of inline buttons
    """

    favorites = db.get_user_movies(message.from_user.id)

    if not favorites:
        await message.answer(template().FAVORITES_LIST_EMPTY)
        return

    markup = FavoritesInlineMarkup(movie_api.movie_factory(favorites))
    await message.answer(text=template().BUTTON_FAVORITES_SHOW, reply_markup=markup)


async def trending(message: types.Message, movie_api: MovieAPI):
    """
    Called on `/trending` command or on the corresponding button in main menu.

    Sends the user a list of 7 currently trending movies in a form of 2 messages:
    - Group of poster photos
    - One text message with brief movies info and inline buttons to retrieve further info
    """

    trending = movie_api.get_trending()

    media_group = MediaGroupBuilder()
    text = ""

    for i, movie in enumerate(trending):
        media_group.add_photo(media=movie.poster_path)
        text += f"<b>{i + 1}.</b> {movie.text_brief}\n"

    await message.answer_media_group(media=media_group.build())
    await message.answer(text, reply_markup=TrendingInlineMarkup(trending))


def setup(dp: Dispatcher):
    dp.message.register(search, Command("search"))
    dp.message.register(search, F.text, SpecialStateMachine.search_input)

    dp.message.register(list_favorites, Command("favorites"))
    dp.message.register(list_favorites, F.text == template().BUTTON_FAVORITES_SHOW)

    dp.message.register(trending, Command("trending"))
    dp.message.register(trending, F.text == template().BUTTON_TRENDING)
