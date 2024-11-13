from aiogram.fsm.state import StatesGroup, State


class Movie:
    """
    Class representing a movie

    Attributes
    ------------
    movie_id: int
        The TMDB ID of the movie
    title: str
        The title of the movie
    genres: str
        The genres of the movie in a comma-separated string
    rating: float
        The rating of the movie
    year: int
        The year of release of the movie
    overview: str
        The overview of the movie
    poster_path: str
        The TMDB API path to the poster of the movie
    trailer_url: str
        The YouTube URL of the trailer of the movie
    """

    def __init__(
        self,
        movie_id: int,
        title: str,
        genres: str,
        rating: float,
        year: int,
        overview: str,
        poster_url: str,
        trailer_url: str = "",
    ):
        self.movie_id = movie_id
        self.title = title
        self.genres = genres
        self.rating = rating
        self.year = year
        self.overview = overview
        self.poster_path = poster_url
        self.trailer_url = trailer_url

    GENRES = {
        28: "Бойовик",
        12: "Пригоди",
        16: "Мультфільм",
        35: "Комедія",
        80: "Кримінал",
        99: "Документальний",
        18: "Драма",
        10751: "Сімейний",
        14: "Фентезі",
        36: "Історичний",
        27: "Жахи",
        10402: "Музика",
        9648: "Детектив",
        10749: "Мелодрама",
        878: "Фантастика",
        10770: "Телефільм",
        53: "Трилер",
        10752: "Військовий",
        37: "Вестерн",
    }

    @property
    def text(self) -> str:
        """
        A formatted text representation of the movie for Telegram

        Returns
        -------
        str
            A formatted text representation of the movie
        """

        result = ""

        result += f"🎬 <b>{self.title}</b>\n\n"

        result += f"⭐️ {self.rating}\n" if self.rating != 0 else f"⭐️ Немає рейтингу\n"
        result += f"📅 {self.year}\n"
        result += f"🎭 {self.genres}\n\n"

        if self.trailer_url:
            result += f'🔗 <a href="{self.trailer_url}">Трейлер (YouTube)</a>\n'
        result += f"<blockquote expandable>{self.overview}</blockquote>\n\n"

        return result

    @classmethod
    def from_api(cls, data: dict):
        """
        Creates a Movie instance from API data.

        Parameters
        ----------
        data : dict
            The API data for the movie.

        Returns
        -------
        Movie
            A Movie instance created from the API data.
        """

        if "genre_ids" in data:
            genre_names = [cls.GENRES[genre_id] for genre_id in data["genre_ids"]]
        elif "genres" in data:
            genre_names = []
            for genre in data["genres"]:
                genre_names.append(genre["name"])
        genres = ", ".join(genre_names).capitalize()

        if data["poster_path"] is not None:
            poster_url = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        else:
            poster_url = None

        rating: float = round(data["vote_average"], 1)

        return cls(
            data["id"],
            data["title"],
            genres,
            rating,
            data["release_date"][:4],  # year
            data["overview"],
            poster_url,
            data["trailer_url"],
        )


class SpecialStateMachine(StatesGroup):
    """
    Class representing a list of special states states for a finite state machine

    Has 3 states:
    - main_menu
    - search_input
    - clear_confirm
    """
    
    search_input = State()
    clear_confirm = State()
