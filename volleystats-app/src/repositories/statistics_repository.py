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

    def get_pass_stats_for_game(self, game_id: int):
        """Get all pass statistics for a game

        Args:
            game_id: ID of the game

        Returns:
            list: List of tuples containing (player_id, score)
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT player_id, score FROM pass_statistics WHERE game_id = ?",
            (game_id,)
        )
        return cursor.fetchall()

    def get_player_pass_stats_for_game(self, game_id: int, player_id: int):
        """Get pass statistics for a specific player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player

        Returns:
            list: List of pass scores for the player
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT score FROM pass_statistics WHERE game_id = ? AND player_id = ?",
            (game_id, player_id)
        )
        return cursor.fetchall()

    def add_serve_stat(self, game_id: int, player_id: int, serve_score: int):
        """Add a serve statistic for a player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player who served
            serve_score: Score of the serve (0-3)
                        0: error, 1: easy serve
                        2: opponent out of system, 3: ace
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "INSERT INTO serve_statistics (game_id, player_id, score) VALUES (?, ?, ?)",
            (game_id, player_id, serve_score)
        )
        self._connection.commit()

    def get_player_serve_stats_for_game(self, game_id: int, player_id: int):
        """Get serve statistics for a specific player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player

        Returns:
            list: List of serve scores for the player
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT score FROM serve_statistics WHERE game_id = ? AND player_id = ?",
            (game_id, player_id)
        )
        return cursor.fetchall()

    def get_game_serve_statistics(self, game_id: int):
        """Get all serve statistics for a game

        Args:
            game_id: ID of the game

        Returns:
            list: List of tuples containing (player_id, score)
        """
        cursor = self._connection.cursor()
        cursor.execute(
            "SELECT player_id, score FROM serve_statistics WHERE game_id = ?",
            (game_id,)
        )
        return cursor.fetchall()
