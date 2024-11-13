from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import Movie
from modules.types.markup import InfoInlineMarkup, SearchResultInlineMarkup


async def show_more_results(
    callback: types.CallbackQuery, state: FSMContext, db: FavoritesDB
):
    other_results: list[Movie] = (await state.get_data())["other_results"]
    await callback.message.answer(Template.MORE_RESULTS_SHOW + str(len(other_results)))

    for result in other_results:
        action = (
            "add"
            if result.movie_id not in db.get_user_movies(callback.from_user.id)
            else "remove"
        )

        markup = InfoInlineMarkup(result.movie_id, favorites_action=action)

        if result.poster_path:
            await callback.message.answer_photo(
                photo=result.poster_path,
                caption=result.text,
                reply_markup=markup,
            )
        else:
            await callback.message.answer(text=result.text, reply_markup=markup)

    await callback.answer(Template.MORE_RESULTS_SHOWN + str(len(other_results)))


async def update_favorites(callback: types.CallbackQuery, db: FavoritesDB):

    # parse callback data
    from_search = callback.data.endswith("|search")
    command = callback.data.removeprefix("favorites_").removesuffix("|search")
    movie_id = int(command.split(":")[1])
    action = command.split(":")[0]

    db.update_movies_in_user(callback.from_user.id, action, movie_id)

    if action == "add":
        await callback.answer(Template.FAVORITES_ADDED_ALERT)
        anti_action = "remove"
    elif action == "remove":
        await callback.answer(Template.FAVORITES_REMOVED_ALERT)
        anti_action = "add"

    # change the inline button respectively: if added, set remove and vice versa
    if from_search:
        markup = SearchResultInlineMarkup(movie_id, anti_action)
    else:
        markup = InfoInlineMarkup(movie_id, anti_action)
    await callback.message.edit_reply_markup(reply_markup=markup)


async def expand_from_favorites(callback: types.CallbackQuery, movie_api: MovieAPI):
    movie_id = int(callback.data.removeprefix("expand:"))
    movie = movie_api.get_movie(movie_id)

    markup = InfoInlineMarkup(movie_id, favorites_action="remove")

    if movie.poster_path:
        await callback.message.answer_photo(
            photo=movie.poster_path,
            caption=movie.text,
            reply_markup=markup,
        )
    else:
        await callback.message.answer(text=movie.text, reply_markup=markup)

    await callback.answer()


def setup(dp: Dispatcher):
    dp.callback_query.register(show_more_results, F.data == "show_more_results")
    dp.callback_query.register(update_favorites, F.data.startswith("favorites"))
    dp.callback_query.register(expand_from_favorites, F.data.startswith("expand"))
