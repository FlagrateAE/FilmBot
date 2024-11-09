class Movie:
    """
    Class representing a movie

    Attributes
    ------------
    movie_id: int
        The TMDB ID of the movie
    title: str
        The title of the movie
    genres: list
        The genres of the movie (not implemented yet)
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
        rating: float,
        year: int,
        overview: str,
        poster_url: str,
        trailer_url: str = "",
    ):
        self.movie_id = movie_id
        self.title = title
        # self.genres =
        self.rating = rating
        self.year = year
        self.overview = overview
        self.poster_path = poster_url
        self.trailer_url = trailer_url

    @property
    def text(self):
        """
        A formatted text representation of the movie for Telegram

        Returns
        -------
        str
            A formatted text representation of the movie
        """

        result = ""

        result += f"🎬 <b>{self.title}</b>\n\n"

        result += f"⭐️ {self.rating}\n"
        result += f"📅 {self.year}\n\n"

        if self.trailer_url:
            result += f'🔗 <a href="{self.trailer_url}">трейлер (YouTube)</a>\n'
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

        poster_url = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        rating: float = round(data["vote_average"], 1)

        return cls(
            data["id"],
            data["title"],
            rating,
            data["release_date"][:4],  # year
            data["overview"],
            poster_url,
            data["trailer_url"],
        )
