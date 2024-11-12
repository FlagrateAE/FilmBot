from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

from modules.messageTemplates import Template
from modules.types.common import Movie


class MainMenuMarkup(ReplyKeyboardMarkup):
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
    def __init__(
        self,
        movie_id: int,
        favorites_action: str,
        from_expand: bool = False,
    ):
        """
        Class representing the inline keyboard markup to display under search result (found movie) message

        Consists of 2 buttons: add the movie to or remove from favorites, show other search results (optional)

        Parameters
        ----------
        movie_id : int
            The ID of the movie
        favorites_action : str
            The action to display on the button: "add" or "remove" a movie from favorites
        from_expand : bool, optional
            Whether the message was derived from "expand" callback (if so, the "show more results" button will not be displayed). Defaults to False.

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

        keyboard = [[favorites_button]]

        if not from_expand:
            keyboard.append(
                [
                    InlineKeyboardButton(
                        text=Template.MORE_RESULTS_BUTTON,
                        callback_data="show_more",
                    )
                ]
            )

        super().__init__(inline_keyboard=keyboard)


class FavouriteListInlineMarkup(InlineKeyboardMarkup):
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
