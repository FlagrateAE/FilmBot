from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext

from modules.movieAPI import MovieAPI
from modules.database import FavoritesDB
from modules.messageTemplates import Template
from modules.types.common import Movie
from modules.types.markup import InfoInlineMarkup, SearchResultInlineMarkup
from modules.handlers.general import _send_movie


async def show_more_results(
    callback: types.CallbackQuery,
    state: FSMContext,
    movie_api: MovieAPI,
    db: FavoritesDB,
):
    """
    Called on a `show_more_results` callback (when user presses "Show more results" button unser a serach result).

    Retureves full search results list from state data and sends them to the user
    """
    other_ids = callback.data.removeprefix("others:").split(",")
    other_results = movie_api.movie_factory(other_ids)
    
    await callback.message.answer(Template.MORE_RESULTS_SHOW + str(len(other_results)))

    for result in other_results:
        action = (
            "add"
            if result.movie_id not in db.get_user_movies(callback.from_user.id)
            else "remove"
        )

        markup = InfoInlineMarkup(result.movie_id, favorites_action=action)

        await _send_movie(callback.message, result, markup)

    await callback.answer(Template.MORE_RESULTS_SHOWN + str(len(other_results)))


async def update_favorites(callback: types.CallbackQuery, db: FavoritesDB):
    """
    Called on a `favorites:<action>:<movie_id>` callback (when user presses "Add to favorites" or "Remove from favorites" button under a movie info).

    Updates user favorite movies list and reverts the callback button (for example, if user adds a movie to favorites, the "Add to favorites" button will be changed to "Remove from favorites")
    """

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


async def expand_from_button(
    callback: types.CallbackQuery,
    movie_api: MovieAPI,
    db: FavoritesDB,
    from_trending: bool = False,
):
    """
    Called on an `expand_<from>:<movie_id>` callback (when user presses a movie button in a favorites or trending lists).
    <from> is either "favorites" or "trending"

    Looks up movie data via API and sends back
    """

    command = callback.data.removeprefix("expand_")
    source = command.split(":")[0]
    movie_id = int(command.split(":")[1])
    movie = movie_api.get_movie(movie_id)

    if source == "trending":
        action = (
            "add"
            if movie_id not in db.get_user_movies(callback.from_user.id)
            else "remove"
        )
    elif source == "favorites":
        # only remove action available
        action = "remove"

    markup = InfoInlineMarkup(movie_id, favorites_action=action)

    await _send_movie(callback.message, movie, markup)

    await callback.answer()


def setup(dp: Dispatcher):
    dp.callback_query.register(show_more_results, F.data.startswith("others:"))
    dp.callback_query.register(update_favorites, F.data.startswith("favorites"))
    dp.callback_query.register(expand_from_button, F.data.startswith("expand"))
