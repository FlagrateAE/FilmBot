import json
import logging
import redis


class FavoritesRedis:
    def __init__(self, host, port, password):
        self.r = redis.StrictRedis(
            host=host, port=port, password=password, decode_responses=True
        )

    def get_user_movies(self, user_id: int) -> list[int]:
        """
        Get the list of favorite movies for a user

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.

        Returns
        -------
        list[int]
            A list of favorite movie IDs.
        """

        favorites = self.r.get(user_id)
        if not favorites:
            return []
        else:
            return json.loads(favorites)
    
    def _set_user_movies(self, user_id: int, movies: list[int]):
        self.r.set(user_id, json.dumps(movies))

    def update_movies_in_user(self, user_id: int, action: str, movie_id: int):
        """
        Update a user's favorite movies list

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.
        action : str
            The action to perform: "add" or "remove" a movie
        movie_id : int
            The ID of the movie to add or remove
        """

        # get current movies
        favorites = self.get_user_movies(user_id)

        if action == "add" and movie_id not in favorites:
            favorites.append(movie_id)

        elif action == "remove" and movie_id in favorites:
            favorites.remove(movie_id)
        
        self._set_user_movies(user_id, favorites)

    def new_user(self, user_id: int):
        self._set_user_movies(user_id, [])
    
    def clear_user_movies(self, user_id: int):
        self.new_user(user_id)