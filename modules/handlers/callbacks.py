from aiogram import Dispatcher, types, F

from ..movieAPI import MovieAPI
from ..database import FavoritesDB
from ..messageTemplates import Template
from ..types import AddToFavoritesMarkup, RemoveFromFavoritesMarkup


async def update_favorites(callback: types.CallbackQuery, db: FavoritesDB):
    command = callback.data.removeprefix("favorites_")

    movie_id = int(command.split(":")[1])
    action = command.split(":")[0]

    db.update_movies_in_user(callback.from_user.id, action, movie_id)

    if action == "add":
        await callback.answer(Template.FAVORITES_ADDED_ALERT)
        markup = RemoveFromFavoritesMarkup(movie_id)
    elif action == "remove":
        await callback.answer(Template.FAVORITES_REMOVED_ALERT)
        markup = AddToFavoritesMarkup(movie_id)

    await callback.message.edit_reply_markup(reply_markup=markup)


async def show_movie_info(callback: types.CallbackQuery, movie_api: MovieAPI):
    movie_id = int(callback.data.removeprefix("expand:"))
    movie = movie_api.get_movie(movie_id)

    markup = RemoveFromFavoritesMarkup(movie_id)

    await callback.message.answer_photo(
        photo=movie.poster_path,
        caption=movie.text,
        reply_markup=markup,
    )

    await callback.answer()


def setup(dp: Dispatcher):
    dp.callback_query.register(update_favorites, F.data.startswith("favorites"))
    dp.callback_query.register(show_movie_info, F.data.startswith("expand"))
