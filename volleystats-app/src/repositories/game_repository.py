import sqlite3
from datetime import datetime
from entities.game import Game
from database_connection import get_database_connection


class GameRepository:
    """Repository class for game data"""

    def __init__(self):
        self._connection = get_database_connection()

    def create_game(self, team_id: int) -> Game:
        """Create a new game for a team

        Args:
            team_id: ID of the team playing

        Returns:
            Game: Created game object
        """
        cursor = self._connection.cursor()
        date = datetime.now().isoformat()

        cursor.execute(
            "INSERT INTO games (date, team_id) VALUES (?, ?)",
            (date, team_id)
        )
        self._connection.commit()

        game_id = cursor.lastrowid
        return Game(team_id, datetime.fromisoformat(date), game_id)

    def get_team_games(self, team_id: int):
        """Get all games for a team

        Args:
            team_id: ID of the team

        Returns:
            list: List of Game objects
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, date FROM games WHERE team_id = ? ORDER BY date DESC",
            (team_id,)
        )

        return [
            Game(team_id, datetime.fromisoformat(row["date"]), row["id"])
            for row in cursor.fetchall()
        ]
