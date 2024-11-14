import sqlite3
import json


class FavoritesDB:
    def __init__(self, db_path):
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

    def new_user(self, user_id: int) -> bool:
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
        else:
            print("User already exists")

    def clear_user_movies(self, user_id: int):
        self.cursor.execute(
            "UPDATE favorites SET movies = ? WHERE user_id = ?",
            ("[]", user_id),
        )
        self.conn.commit()

    def get_all(self):
        self.cursor.execute("SELECT * FROM favorites")
        return self.cursor.fetchall()
