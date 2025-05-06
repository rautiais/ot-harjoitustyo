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
            "INSERT INTO games (date, team_id, status) VALUES (?, ?, ?)",
            (date, team_id, "ongoing")
        )
        self._connection.commit()

        game_id = cursor.lastrowid
        return Game(team_id, datetime.fromisoformat(date), game_id, "ongoing")

    def get_team_games(self, team_id: int):
        """Get all games for a team

        Args:
            team_id: ID of the team

        Returns:
            list: List of Game objects
        """
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, date, status FROM games WHERE team_id = ? ORDER BY date DESC",
            (team_id,)
        )

        games = []
        for row in cursor.fetchall():
            game = Game(
                team_id=team_id,
                date=datetime.fromisoformat(row[1]),
                game_id=row[0],
                status=row[2]
            )
            games.append(game)
        return games

    def update_game_status(self, game_id: int, status: str):
        """Update game status

        Args:
            game_id: ID of the game
            status: New status for the game ('ongoing' or 'ended')
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "UPDATE games SET status = ? WHERE id = ?",
            (status, game_id)
        )
        self._connection.commit()
