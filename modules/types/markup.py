from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

import modules.messageTemplates as template
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
                    KeyboardButton(text=template.BUTTON_SEARCH),
                ],
                [
                    KeyboardButton(text=template.BUTTON_FAVORITES_SHOW),
                    KeyboardButton(text=template.BUTTON_TRENDING),
                ],
                [
                    KeyboardButton(text=template.BUTTON_FAVORITES_CLEAR),
                    KeyboardButton(text=template.BUTTON_HELP),
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
                text=template.BUTTON_FAVORITES_ADD,
                callback_data=f"favorites_add:{movie_id}",
            )
        elif favorites_action == "remove":
            favorites_button = InlineKeyboardButton(
                text=template.BUTTON_FAVORITES_REMOVE,
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

    def __init__(
        self,
        movie_id: int,
        favorites_action: str = "add",
        other_results_ids: list[int] = [],
    ):
        """
        Parameters
        ----------
        movie_id : int
            The ID of the movie.
        favorites_action : str
            Either "add" or "remove"
        other_results_ids : list[int]
            If used from search, list of unshown results (moviis IDs)  to show when corresponding button is pressed
        """

        super().__init__(movie_id, favorites_action)

        ids = ",".join(map(str, other_results_ids))
        # mark the buttons as from search
        self.inline_keyboard[0][0].callback_data += "|search"

        self.inline_keyboard.append(
            [
                InlineKeyboardButton(
                    text=template.BUTTON_SHOW_MORE,
                    callback_data="others:" + ids,
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

        # This is a pretty inline keyboard layout for 7 buttons (representing 7 trending movies). The layout is as it is because of how Telegram lays out a group of images (those are posters images corresponding to buttons)
        INLINE_KEYBOARD_LAYOUT = [[0, 1], [2, 3], [4, 5, 6]]

        keyboard = []

        for layout_row in INLINE_KEYBOARD_LAYOUT:
            row = []
            for i in layout_row:
                row.append(
                    InlineKeyboardButton(
                        text=movies[i].title,
                        callback_data=f"expand_trending:{movies[i].movie_id}",
                    )
                )
            keyboard.append(row)

        super().__init__(inline_keyboard=keyboard)


class ClearConfirmMarkup(ReplyKeyboardMarkup):
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
                    KeyboardButton(text=template.BUTTON_CLEAR_CONFIRM),
                    KeyboardButton(text=template.BUTTON_CLEAR_CANCEL),
                ],
            ],
            resize_keyboard=True,
        )
