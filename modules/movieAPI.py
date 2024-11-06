import requests
from modules.types import Movie


class MovieAPI:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, access_token: str):
        self.HEADERS = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
        }

    def search(self, query: str, language: str = "uk-UA", include_adult: bool = False):
        url = self.BASE_URL + "/search/movie"
        
        params = {
                "query": query,
                "language": language,
                "include_adult": str(include_adult)
            }

        results = requests.get(url, params, headers=self.HEADERS).json()["results"]
        best_match = Movie.from_api(results[0])
        
        return best_match
