import json
import redis


class FavoritesRedis:
    """
    Class to interact with the Redis database of users` favorite movies.

    Methods
    -------
    get_user_movies(user_id)
        Get the list of favorite movies for a user
    _set_user_movies(user_id, movies)
        Set the list of favorite movies for a user (internal)        
    update_movies_in_user(user_id, action, movie_id)
        Update a user's favorite movies list
    new_user(user_id)
        Create a new user with an empty movies list (on /start command)
    clear_user_movies(user_id)
        Clear a user's favorite movies list
    """
    
    def __init__(self, host, port, password = None):
        """
        Initialize the Redis connection

        Parameters
        host: str
            The hostname of the Redis server
        port: int
            The port number of the Redis server
        password: str
            The password of the Redis. Default is None.
        """
        
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
        """
        Set the list of favorite movies for a user (internal)

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.
        movies : list[int]
            A list of favorite movie IDs.
        """
        
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

        current_favorites = self.get_user_movies(user_id)

        if action == "add" and movie_id not in current_favorites:
            current_favorites.append(movie_id)

        elif action == "remove" and movie_id in current_favorites:
            current_favorites.remove(movie_id)
        
        self._set_user_movies(user_id, current_favorites)

    def new_user(self, user_id: int):
        """
        Create a new user with an empty movies list (on /start command)

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.
        """
        
        self._set_user_movies(user_id, [])
    
    def clear_user_movies(self, user_id: int):
        """
        Clear a user's favorite movies list. Uses the new_user method.

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.
        """
        
        self.new_user(user_id)