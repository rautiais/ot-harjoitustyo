import sqlite3
from entities.user import User
from database_connection import get_database_connection


class UserRepository:
    def __init__(self):
        self._connection = get_database_connection()

    def create_user(self, username: str, password: str):
        cursor = self._connection.cursor()
        try:
            cursor.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, password)
            )
            self._connection.commit()

            cursor.execute(
                "SELECT id FROM users WHERE username=?",
                (username,)
            )
            user_id = cursor.fetchone()["id"]
            return User(username, password, user_id)
        except sqlite3.IntegrityError:
            return None

    def find_by_username(self, username: str):
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT id, username, password FROM users WHERE username=?",
            (username,)
        )
        row = cursor.fetchone()
        return User(row["username"], row["password"], row["id"]) if row else None

    def delete_all(self):
        """Delete all users from the database."""
        cursor = self._connection.cursor()
        cursor.execute("DELETE FROM users")
        self._connection.commit()
