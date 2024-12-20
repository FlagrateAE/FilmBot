import requests
from modules.types.common import Movie


class MovieAPI:
    """
    Class for interacting with The Movie Database API.

    This class handles HTTP requests to the TMDB API and returns movie information.

    Attributes
    ----------
    BASE_URL : str
        The base URL for the TMDB API.
    headers : dict
        The headers for the HTTP request.

    Methods
    -------
    api_call(endpoint, params) -> dict
        Makes an HTTP GET request to the TMDB API.

    search(query) -> Movie | None
        Searches for a movie using the specified query and returns the best match.

    get_trailer_url(movie_id) -> str | None
        Finds and returns a YouTube URL for a movie trailer in default language (if any) or in English.
    """

    BASE_URL = "https://api.themoviedb.org/3"
    LANGUAGE = "uk-UA"

    def __init__(self, access_token: str):
        """
        Initialize the MovieAPI class.

        Parameters
        ----------
        access_token : str
            The access token for the TMDB API.
        """
        self.headers = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
        }

    def api_call(self, endpoint: str, params: dict = {}) -> dict:
        """
        Makes an HTTP GET request to the TMDB API.

        Parameters
        ----------
        endpoint : str
            The endpoint of the TMDB API in the format "/<endpoint>".
        params : dict, optional
            The query parameters for the HTTP request.

        Returns
        -------
        dict
            The response from the TMDB API.
        """

        url = self.BASE_URL + endpoint
        response = requests.get(url, params, headers=self.headers)

        return response.json()

    def search(self, query: str) -> list[Movie] | None:
        """
        Searches for a movie using the specified query and returns the best match.

        Parameters
        ----------
        query : str
            The query to search for.

        Returns
        -------
        Movie | None
            The best match movie, or None if no results were found.
        """

        search_results: list[dict] = self.api_call(
            endpoint="/search/movie",
            params={"query": query, "language": self.LANGUAGE},
        )["results"]

        if not search_results:
            return None

        movies = []
        for movie_data in search_results[:6]:
            # only first 6 results (1 shown immedeiately, 5 more on show_more_results button)
            trailer_url = self.get_trailer_url(movie_data["id"])
            movie_data["trailer_url"] = trailer_url
            movies.append(Movie.from_api(movie_data))

        return movies

    def get_trending(self) -> list[Movie]:
        """
        Returns a list of currently trending movies.

        Returns
        -------
        list[Movie]
            A list of Movie objects representing the currently trending movies
        """

        # Limit is set to 7. Changing it, be sure to change the inline keyboard layout in TrendingInlineMarkup in modules/types/markup.py
        MAX_RESULTS = 7

        trending = self.api_call(
            endpoint="/trending/movie/week",
            params={"language": self.LANGUAGE},
        )["results"]

        movies = []
        for movie_data in trending[:MAX_RESULTS]:
            trailer_url = self.get_trailer_url(movie_data["id"])
            movie_data["trailer_url"] = trailer_url
            movies.append(Movie.from_api(movie_data))

        return movies

    def get_trailer_url(self, movie_id: int) -> str | None:
        """
        Finds and returns a YouTube URL for a movie trailer in default language (if any) or in English.

        Parameters
        ----------
        movie_id : int
            The TMDB ID of the movie.

        Returns
        -------
        str | None
            The YouTube URL for the movie trailer, or None if no trailer was found.
        """
        videos = self.api_call(
            endpoint=f"/movie/{movie_id}/videos",
            params={"language": self.LANGUAGE},
        )["results"]

        if not videos:
            # if no trailer found in default language, try English
            videos = self.api_call(
                endpoint=f"/movie/{movie_id}/videos",
                params={"language": "en-US"},
            )["results"]

        for video in videos:
            if video["type"] == "Trailer" and video["site"] == "YouTube":
                return f"https://www.youtube.com/watch?v={video['key']}"

        return None

    def get_movie(self, movie_id: int) -> Movie:
        """
        Returns a Movie object for the specified TMDB ID.

        Parameters
        ----------
        movie_id : int
            The TMDB ID of the movie.

        Returns
        -------
        Movie
            A Movie object for the specified TMDB ID.
        """
        movie_data = self.api_call(
            endpoint=f"/movie/{movie_id}", params={"language": self.LANGUAGE}
        )
        movie_data["trailer_url"] = self.get_trailer_url(movie_id)

        return Movie.from_api(movie_data)

    def movie_factory(self, movie_ids: list[int]) -> list[Movie]:
        """
        Returns a list of Movie objects for the specified list of TMDB IDs.

        Parameters
        ----------
        movie_ids : list[int]
            A list of TMDB IDs of the movies.

        Returns
        -------
        list[Movie]
            A list of Movie objects for the specified list of TMDB IDs.
        """
        return [self.get_movie(movie_id) for movie_id in movie_ids]
