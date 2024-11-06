class Movie():
    def __init__(self, title: str, rating: float, year: int, overview: str, poster_path: str):
        self.title = title
        # self.genres = 
        self.rating = rating
        self.year = year
        self.overview = overview
        self.poster_path = poster_path
        
    @property
    def text(self):
        result = ""
        
        result += f"🎬 <b>{self.title}</b>\n\n"
        result += f"⭐️ {self.rating}\n"
        result += f"📅 {self.year}\n\n"
        result += f"<blockquote expandable>{self.overview}</blockquote>\n\n"
        
        return result
    
    @classmethod
    def from_api(cls, data: dict):
        return cls(
            data["title"],
            data["vote_average"],
            data["release_date"][:4],
            data["overview"],
            data["poster_path"]
        )