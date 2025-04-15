import sqlite3
from config import DATABASE_FILE_PATH


class DatabaseConnection:
    """Class for managing database connections"""

    def __init__(self):
        self._connection = None
        self._database_path = DATABASE_FILE_PATH

    def get_database_connection(self):
        """Returns a database connection, creating it if necessary"""
        if not self._connection:
            self._connection = sqlite3.connect(self._database_path)
            self._connection.row_factory = sqlite3.Row

        return self._connection

    def close_connection(self):
        """Closes the database connection if it exists"""
        if self._connection:
            self._connection.close()
            self._connection = None

    def set_database_path(self, path):
        """Sets the database path and closes any existing connection"""
        self.close_connection()
        self._database_path = path


# Create singleton instance
_connection_manager = DatabaseConnection()

# Public interface


def get_database_connection():
    """Returns a database connection"""
    return _connection_manager.get_database_connection()


def close_connection():
    """Closes the current database connection"""
    _connection_manager.close_connection()


def set_database_path(path):
    """Sets the database path"""
    _connection_manager.set_database_path(path)
