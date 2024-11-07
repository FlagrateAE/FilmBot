class Movie:
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
        poster_url = f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
        rating: float = round(data["vote_average"], 1)

        return cls(
            data["id"],
            data["title"],
            rating,
            data["release_date"][:4],  # year
            data["overview"],
            poster_url,
            data["trailer_url"]
        )
