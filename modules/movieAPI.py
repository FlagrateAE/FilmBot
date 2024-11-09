import requests
from modules.types import Movie


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

    search(query, language, include_adult) -> Movie | None
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

    def search(
        self, query: str, language: str = "uk-UA", include_adult: bool = False
    ) -> Movie | None:
        """
        Searches for a movie using the specified query and returns the best match.

        Parameters
        ----------
        query : str
            The query to search for.
        language : str, optional
            The language to search in. Defaults to "uk-UA" (Ukrainian).
        include_adult : bool, optional
            Whether to include adult movies in the search results. Defaults to False.

        Returns
        -------
        Movie | None
            The best match movie, or None if no results were found.
        """

        searchResults = self.api_call(
            endpoint="/search/movie",
            params={
                "query": query,
                "language": language,
                "include_adult": str(include_adult),
            },
        )["results"]

        if not searchResults:
            return None

        best_match = searchResults[0]
        trailer_url = self.get_trailer_url(best_match["id"], language)
        best_match["trailer_url"] = trailer_url

        return Movie.from_api(best_match)

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
