import os
import sqlite3

DIRNAME = os.path.dirname(__file__)
DB_FILE_PATH = os.path.join(DIRNAME, "..", "data", "database.sqlite")


def get_database_connection():
    connection = sqlite3.connect(DB_FILE_PATH)
    connection.row_factory = sqlite3.Row
    return connection
