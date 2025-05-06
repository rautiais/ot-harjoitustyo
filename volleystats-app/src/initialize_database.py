from database_connection import get_database_connection, close_connection


def drop_tables(connection):
    """"Drops tables if they exist."""
    cursor = connection.cursor()
    cursor.execute('''DROP TABLE IF EXISTS teams''')
    cursor.execute('''DROP TABLE IF EXISTS users''')
    cursor.execute('''DROP TABLE IF EXISTS players''')
    cursor.execute('''DROP TABLE IF EXISTS games''')
    cursor.execute('''DROP TABLE IF EXISTS pass_statistics''')
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
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS teams (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            number INTEGER,
            team_id INTEGER NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY,
            date TEXT NOT NULL,
            team_id INTEGER NOT NULL,
            FOREIGN KEY (team_id) REFERENCES teams (id)
        );
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pass_statistics (
            id INTEGER PRIMARY KEY,
            game_id INTEGER NOT NULL,
            player_id INTEGER NOT NULL,
            score INTEGER NOT NULL,
            FOREIGN KEY (game_id) REFERENCES games (id),
            FOREIGN KEY (player_id) REFERENCES players (id)
        );
    ''')

    connection.commit()


def initialize_database():
    """Initializes database"""
    connection = get_database_connection()
    drop_tables(connection)
    create_tables(connection)
    close_connection()


if __name__ == "__main__":
    initialize_database()
