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
    ):

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
    def __init__(self, movie_id: int, favorites_action: str = "add"):
        super().__init__(movie_id, favorites_action)

        self.inline_keyboard[0][0].callback_data += "|search"

        self.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=Template.MORE_RESULTS_BUTTON,
                    callback_data="more_results",
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
                        callback_data=f"expand:{movie.movie_id}",
                    )
                ]
                for movie in movies
            ]
        )
