import requests
from modules.types.common import Movie


class MovieAPI:
    """
    Class for interacting with The Movie Database API.

    This class handles HTTP requests to the TMDB API and returns movie information.

    Parameters
    ----------
    access_token : str
        The access token for the TMDB API.

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

    search(query, language) -> Movie | None
        Searches for a movie using the specified query and returns the best match.

    get_trailer_url(movie_id, language) -> str | None
        Finds and returns a YouTube URL for a movie trailer in the specified language.
    """

    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, access_token: str):
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

    def search(self, query: str, language: str = "uk-UA") -> list[Movie] | None:
        """
        Searches for a movie using the specified query and returns the best match.

        Parameters
        ----------
        query : str
            The query to search for.
        language : str, optional
            The language to search in. Defaults to "uk-UA" (Ukrainian).

        Returns
        -------
        Movie | None
            The best match movie, or None if no results were found.
        """

        search_results: list[dict] = self.api_call(
            endpoint="/search/movie",
            params={
                "query": query,
                "language": language,
            },
        )["results"]

        if not search_results:
            return None

        movies = []
        for movie_data in search_results[:6]:
            # only first 6 results (1 shown immedeiately, 5 more on show_more_results button)
            trailer_url = self.get_trailer_url(movie_data["id"], language)
            movie_data["trailer_url"] = trailer_url
            movies.append(Movie.from_api(movie_data))

        return movies

    def get_trending(self, language: str = "uk-UA") -> list[Movie]:
        """
        Returns a list of currently trending movies.

        Parameters
        ----------
        language : str, optional
            The language to search in. Defaults to "uk-UA" (Ukrainian).

        Returns
        -------
        list[Movie]
            A list of Movie objects representing the currently trending movies
        """

        trending = self.api_call(
            endpoint="/trending/movie/week",
            params={
                "language": language,
            },
        )["results"]

        movies = []
        for movie_data in trending[:7]:
            trailer_url = self.get_trailer_url(movie_data["id"], language)
            movie_data["trailer_url"] = trailer_url
            movies.append(Movie.from_api(movie_data))

        return movies

    def get_trailer_url(self, movie_id: int, language: str = "uk-UA") -> str | None:
        """
        Finds and returns a YouTube URL for a movie trailer in the specified language.

        Parameters
        ----------
        movie_id : int
            The TMDB ID of the movie.
        language : str, optional
            The language to search in. Defaults to "uk-UA" (Ukrainian).

        Returns
        -------
        str | None
            The YouTube URL for the movie trailer, or None if no trailer was found.
        """
        videos = self.api_call(
            endpoint=f"/movie/{movie_id}/videos",
            params={"language": language},
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

    def get_movie(self, movie_id: int, language: str = "uk-UA") -> Movie:
        """
        Returns a Movie object for the specified TMDB ID.

        Parameters
        ----------
        movie_id : int
            The TMDB ID of the movie.
        language : str, optional
            The language to search in. Defaults to "uk-UA" (Ukrainian).

        Returns
        -------
        Movie
            A Movie object for the specified TMDB ID.
        """
        movie_data = self.api_call(
            endpoint=f"/movie/{movie_id}", params={"language": language}
        )
        movie_data["trailer_url"] = self.get_trailer_url(movie_id, language)

        return Movie.from_api(movie_data)

    def movie_factory(
        self, movie_ids: list[int], language: str = "uk-UA"
    ) -> list[Movie]:
        """
        Returns a list of Movie objects for the specified list of TMDB IDs.

        Parameters
        ----------
        movie_ids : list[int]
            A list of TMDB IDs of the movies.
        language : str, optional
            The language to search in. Defaults to "uk-UA" (Ukrainian).

        Returns
        -------
        list[Movie]
            A list of Movie objects for the specified list of TMDB IDs.
        """
        return [self.get_movie(movie_id, language) for movie_id in movie_ids]
