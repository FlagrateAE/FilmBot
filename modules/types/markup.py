from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from modules.messageTemplates import Template
from modules.types.movie import Movie


class FavouritesInlineMarkup(InlineKeyboardMarkup):
    def __init__(self, movies: list[Movie]):
        """
        Class representing the inline keyboard markup for displaying a list of favorite movies in form of buttons

        Used as an answer to the `/favorites` command

        Parameters
        ----------
        movies : list[Movie]
            A list of Movie objects
        """

        super().__init__(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=movie.title,
                        callback_data=f"expand:{movie.movie_id}",
                    )
                ]
                for movie in movies
            ]
        )


class AddInlineButton(InlineKeyboardButton):
    def __init__(self, movie_id: int):
        """
        Class representing an inline callback button to add a movie to favorites

        Parameters
        ----------
        movie_id : int
            The ID of the movie to add
        """

        super().__init__(
            text=Template.FAVORITES_ADD_BUTTON,
            callback_data=f"favorites_add:{movie_id}",
        )


class RemoveInlineButton(InlineKeyboardButton):
    def __init__(self, movie_id: int):
        """
        Class representing an inline callback button to remove a movie from favorites

        Parameters
        ----------
        movie_id : int
            The ID of the movie to remove
        """

        super().__init__(
            text=Template.FAVORITES_REMOVE_BUTTON,
            callback_data=f"favorites_remove:{movie_id}",
        )


class SearchResultInlineMarkup(InlineKeyboardMarkup):
    def __init__(self, favouritesButton: AddInlineButton | RemoveInlineButton):
        """
        Class representing the inline keyboard markup ot display under search result (found movie) message

        Parameters
        ----------
        favouritesButton : AddInlineButton | RemoveInlineButton
            The button to add or remove movie from favorites
        """

        super().__init__(
            inline_keyboard=[[favouritesButton]],
        )
