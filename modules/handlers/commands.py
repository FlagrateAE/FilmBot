from aiogram import Dispatcher, types
from aiogram.filters.command import Command, CommandObject

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.markup import (
    SearchResultInlineMarkup,
    AddInlineButton,
    FavouritesInlineMarkup,
)

async def start(message: types.Message, db: FavoritesDB):
    try:
        db.new_user(message.from_user.id)
        await message.answer(Template.START)
    except:
        await message.answer(Template.START_DB_ERROR)


async def search(message: types.Message, command: CommandObject, movie_api: MovieAPI):
    if command.args:
        search_result = movie_api.search(query=command.args)

        if not search_result:
            await message.answer(Template.SEARCH_NOT_FOUND)
            return

        markup = SearchResultInlineMarkup(AddInlineButton(search_result.movie_id))

        await message.answer_photo(
            photo=search_result.poster_path,
            caption=search_result.text,
            reply_markup=markup,
        )
    else:
        await message.answer(Template.SEARCH_NO_ARGS)


async def list_favorites(message: types.Message, movie_api: MovieAPI, db: FavoritesDB):
    favorites = db.get_user_movies(message.from_user.id)

    if not favorites:
        await message.answer(Template.FAVORITES_EMPTY)
        return

    markup = FavouritesInlineMarkup(movie_api.movie_factory(favorites))

    await message.answer(Template.FAVORITES_SHOW, reply_markup=markup)


async def _all(message: types.Message, db: FavoritesDB):
    """Used for db testing and output. Will be removed in prod or kept for admins"""
    await message.answer(str(db.get_all()))


def setup(dp: Dispatcher):
    dp.message.register(start, Command("start"))
    dp.message.register(search, Command("search"))
    dp.message.register(list_favorites, Command("favorites"))
    dp.message.register(_all, Command("all"))
