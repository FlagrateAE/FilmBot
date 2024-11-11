from aiogram import Dispatcher, types, F

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.markup import (
    AddInlineButton,
    RemoveInlineButton,
    SearchResultInlineMarkup,
)


async def update_favorites(callback: types.CallbackQuery, db: FavoritesDB):
    command = callback.data.removeprefix("favorites_")

    movie_id = int(command.split(":")[1])
    action = command.split(":")[0]

    db.update_movies_in_user(callback.from_user.id, action, movie_id)

    if action == "add":
        await callback.answer(Template.FAVORITES_ADDED_ALERT)
        markup = SearchResultInlineMarkup(RemoveInlineButton(movie_id))
    elif action == "remove":
        await callback.answer(Template.FAVORITES_REMOVED_ALERT)
        markup = SearchResultInlineMarkup(AddInlineButton(movie_id))


    await callback.message.edit_reply_markup(reply_markup=markup)


async def expand_from_favorites(callback: types.CallbackQuery, movie_api: MovieAPI):
    movie_id = int(callback.data.removeprefix("expand:"))
    movie = movie_api.get_movie(movie_id)

    markup = SearchResultInlineMarkup(RemoveInlineButton(movie_id))

    await callback.message.answer_photo(
        photo=movie.poster_path,
        caption=movie.text,
        reply_markup=markup,
    )

    await callback.answer()


def setup(dp: Dispatcher):
    dp.callback_query.register(update_favorites, F.data.startswith("favorites"))
    dp.callback_query.register(expand_from_favorites, F.data.startswith("expand"))
