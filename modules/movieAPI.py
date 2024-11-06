import requests


class MovieAPI:
    BASE_URL = "https://api.themoviedb.org/3"

    def __init__(self, access_token: str):
        self.HEADERS = {
            "Authorization": "Bearer " + access_token,
            "Accept": "application/json",
        }

    def search(self, query: str, language: str = "uk-UA", include_adult: bool = False):
        url = self.BASE_URL + "/search/movie"

        response = requests.get(url, params={
                "query": query,
                "language": language,
                "include_adult": str(include_adult)
            }, headers=self.HEADERS)
        
        return response.text
