from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from modules.messageTemplates import Template
from modules.types.common import Movie


class MainMenuMarkup(ReplyKeyboardMarkup):
    """
    Class representing a keyboard markup for the main menu.

    Consists of 5 buttons:
    - Search for a movie
    - Show favorites list
    - Show trending movies
    - Clear favorites list
    - Help
    """

    def __init__(self):
        super().__init__(
            keyboard=[
                [
                    KeyboardButton(text=Template.SEARCH_BUTTON),
                ],
                [
                    KeyboardButton(text=Template.FAVORITES_SHOW_BUTTON),
                    KeyboardButton(text=Template.TRENDING_BUTTON),
                ],
                [
                    KeyboardButton(text=Template.FAVORITES_CLEAR_BUTTON),
                    KeyboardButton(text=Template.HELP_BUTTON),
                ],
            ],
            resize_keyboard=True,
        )


class InfoInlineMarkup(InlineKeyboardMarkup):
    """
    Class representing an inline keyboard markup to display under a movie info

    Consists of a single button with either "Add to favorites" or "Remove from favorites"
    """

    def __init__(
        self,
        movie_id: int,
        favorites_action: str,
    ):
        """
        Parameters
        ----------
        movie_id : int
            The ID of the movie.
        favorites_action : str
            Either "add" or "remove"
        """

        if favorites_action == "add":
            favorites_button = InlineKeyboardButton(
                text=Template.FAVORITES_ADD_BUTTON,
                callback_data=f"favorites_add:{movie_id}",
            )
        elif favorites_action == "remove":
            favorites_button = InlineKeyboardButton(
                text=Template.FAVORITES_REMOVE_BUTTON,
                callback_data=f"favorites_remove:{movie_id}",
            )

        super().__init__(inline_keyboard=[[favorites_button]])


class SearchResultInlineMarkup(InfoInlineMarkup):
    """
    Class representing an inline keyboard markup to display under a movie info dervied from search

    Conists of 2 buttons:
    - Either "Add to favorites" or "Remove from favorites"
    - "Show more results"
    """

    def __init__(self, movie_id: int, favorites_action: str = "add"):
        """
        Parameters
        ----------
        movie_id : int
            The ID of the movie.
        favorites_action : str
            Either "add" or "remove"
        """

        super().__init__(movie_id, favorites_action)

        self.inline_keyboard[0][0].callback_data += "|search"

        self.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=Template.MORE_RESULTS_BUTTON,
                    callback_data="show_more_results",
                )
            ]
        )


class FavoritesInlineMarkup(InlineKeyboardMarkup):
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
                        callback_data=f"expand_favorites:{movie.movie_id}",
                    )
                ]
                for movie in movies
            ]
        )


class TrendingInlineMarkup(InlineKeyboardMarkup):
    def __init__(self, movies: list[Movie]):
        """
        Class representing the inline keyboard markup for displaying a list of 7 trending movies in form of buttons

        Used as an answer to the `/trending` command

        Parameters
        ----------
        movies : list[Movie]
            A list of 7 Movie objects representing trending now movies
        """

        super().__init__(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text=movies[0].title,
                        callback_data=f"expand_trending:{movies[0].movie_id}",
                    ),
                    InlineKeyboardButton(
                        text=movies[1].title,
                        callback_data=f"expand_trending:{movies[1].movie_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=movies[2].title,
                        callback_data=f"expand_trending:{movies[2].movie_id}",
                    ),
                    InlineKeyboardButton(
                        text=movies[3].title,
                        callback_data=f"expand_trending:{movies[3].movie_id}",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text=movies[4].title,
                        callback_data=f"expand_trending:{movies[4].movie_id}",
                    ),
                    InlineKeyboardButton(
                        text=movies[5].title,
                        callback_data=f"expand_trending:{movies[5].movie_id}",
                    ),
                    InlineKeyboardButton(
                        text=movies[6].title,
                        callback_data=f"expand_trending:{movies[6].movie_id}",
                    ),
                ],
            ]
        )


class FavoritesClearMarkup(ReplyKeyboardMarkup):
    """
    Class representing a keyboard markup for user to make a decision wheter to clear their favorites list

    Consists of a 2 buttons:
    - Approve
    - Disapprove
    """

    def __init__(self):
        super().__init__(
            keyboard=[
                [
                    KeyboardButton(text=Template.CLEAR_YES_BUTTON),
                    KeyboardButton(text=Template.CLEAR_NO_BUTTON),
                ],
            ],
            resize_keyboard=True,
        )
