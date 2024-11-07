import requests
from modules.types import Movie


class MovieAPI:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, access_token: str):
        self.HEADERS = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
        }

    def api_call(self, endpoint: str, params: dict = {}) -> dict:
        url = self.BASE_URL + endpoint
        response = requests.get(url, params, headers=self.HEADERS)

        return response.json()

    def search(self, query: str, language: str = "uk-UA", include_adult: bool = False):
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
