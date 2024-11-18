import sqlite3
import json
import logging


class FavoritesDB:
    """
    Class to interact with the SQLite database.

    Attributes
    ----------
    db_path : str
        The path to the database file.

    Methods
    -------
    init_db()
        Initialize the database and create the favorites table if it doesn't exist.
    update_movies_in_user(user_id, action, movie_id)
        Update a user's favorite movies list
    get_user_movies(user_id)
        Get the list of favorite movies for a user
    new_user(user_id)
        Create a new user with an empty movies list (on /start command)
    clear_user_movies(user_id)
        Clear a user's favorite movies list
    get_all()
        Get all users and their favorite movies (admin command)
    """

    def __init__(self, db_path):
        """
        Initialize the FavoritesDB class

        Parameters
        ----------
        db_path : str
            The path to the database file.
        """
        
        self.db_path = db_path
        self.init_db()

    def init_db(self):
        """Initialize the database and create the favorites table if it doesn't exist."""

        with sqlite3.connect(self.db_path) as conn:
            self.conn = conn
            self.cursor = conn.cursor()

            self.cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS favorites (
                    user_id INTEGER PRIMARY KEY,
                    movies TEXT
                )
            """
            )
            conn.commit()

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
        self.cursor.execute(
            "SELECT movies FROM favorites WHERE user_id = ?", (user_id,)
        )
        result = self.cursor.fetchone()
        favorite = json.loads(result[0])

        # perform action
        if action == "add":
            if movie_id not in favorite:
                favorite.append(movie_id)

        elif action == "remove":
            if movie_id in favorite:
                favorite.remove(movie_id)

        # update the database
        self.cursor.execute(
            "UPDATE favorites SET movies = ? WHERE user_id = ?",
            (json.dumps(favorite), user_id),
        )
        self.conn.commit()

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
        self.cursor.execute(
            "SELECT movies FROM favorites WHERE user_id = ?", (user_id,)
        )
        result = self.cursor.fetchone()

        if result:
            return json.loads(result[0])
        return None

    def new_user(self, user_id: int):
        """
        Create a new user with an empty movies list (on /start command)

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.
        """
        
        if self.get_user_movies(user_id) == None:
            self.cursor.execute(
                "INSERT INTO favorites (user_id, movies) VALUES (?, ?)",
                (user_id, "[]"),
            )
            self.conn.commit()
            logging.info(f"New user: {user_id}")


    def clear_user_movies(self, user_id: int):
        """
        Clear a user's favorite movies list

        Parameters
        ----------
        user_id : int
            The Telegram ID of the user.
        """
        
        self.cursor.execute(
            "UPDATE favorites SET movies = ? WHERE user_id = ?",
            ("[]", user_id),
        )
        self.conn.commit()

    def get_all(self) -> list[tuple[int, list[int]]]:
        """
        Get all users and their favorite movies (admin command). Use during development and at low scales of the database because of message length limitation.

        Returns
        -------
        list[tuple[int, list[int]]]
            A list of tuples containing user IDs and their favorite movie IDs.
        """
        
        self.cursor.execute("SELECT * FROM favorites")
        return self.cursor.fetchall()
