from aiogram import Dispatcher, types, F
from aiogram.filters.command import Command, CommandObject
from aiogram.fsm.context import FSMContext

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import StateMachine
from modules.types.markup import SearchResultInlineMarkup, FavoritesInlineMarkup


async def search(
    message: types.Message,
    state: FSMContext,
    movie_api: MovieAPI,
    db: FavoritesDB,
    command: CommandObject = None,
):
    if command:
        if command.args:
            query = command.args
        else:
            await message.answer(Template.SEARCH_NO_ARGS)
    else:
        query = message.text

    best_result = movie_api.search(query)[0]
    print(best_result.poster_path)

    if not best_result:
        await message.answer(Template.SEARCH_NOT_FOUND)
        return

    action = (
        "add"
        if best_result.movie_id not in db.get_user_movies(message.from_user.id)
        else "remove"
    )

    markup = SearchResultInlineMarkup(
        movie_id=best_result.movie_id, favorites_action=action
    )
    
    if best_result.poster_path:
        await message.answer_photo(
            photo=best_result.poster_path,
            caption=best_result.text,
            reply_markup=markup,
        )
    else:
        await message.answer(text=best_result.text, reply_markup=markup)
    
    await state.set_state(StateMachine.main_menu)


async def list_favorites(message: types.Message, movie_api: MovieAPI, db: FavoritesDB):
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
