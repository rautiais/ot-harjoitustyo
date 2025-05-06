from database_connection import get_database_connection


class StatisticsRepository:
    def __init__(self):
        self._connection = get_database_connection()

    def add_pass_stat(self, game_id: int, player_id: int, pass_score: int):
        """Add a pass statistic for a player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player who made the pass
            pass_score: Score of the pass (0-3)
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO pass_statistics (game_id, player_id, score) VALUES (?, ?, ?)",
            (game_id, player_id, pass_score)
        )
        self._connection.commit()

    def get_game_statistics(self, game_id: int):
        """Get all pass statistics for a game

        Args:
            game_id: ID of the game

        Returns:
            List of tuples containing (player_id, score)
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT player_id, score FROM pass_statistics WHERE game_id = ?",
            (game_id,)
        )
        return cursor.fetchall()
