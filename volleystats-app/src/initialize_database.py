from database_connection import get_database_connection


def drop_tables(connection):
    """"Drops tables if they exist."""
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS users''')
    connection.commit()


def create_tables(connection):
    """Creates new tables"""
    cursor = connection.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
        );
    ''')
    connection.commit()


def initialize_database():
    """Initializes database"""
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)


if __name__ == "__main__":
    initialize_database()
