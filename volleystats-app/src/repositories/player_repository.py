from entities.player import Player
from database_connection import get_database_connection


class PlayerRepository:
    def __init__(self):
        self._connection = get_database_connection()

    def create_player(self, name: str, number: int, team_id: int):
        cursor = self._connection.cursor()

        cursor.execute(
            "INSERT INTO players (name, number, team_id) VALUES (?, ?, ?)",
            (name, number, team_id)
        )
        self._connection.commit()

        cursor.execute(
            "SELECT id FROM players WHERE name = ? AND number = ? AND team_id = ?",
            (name, number, team_id)
        )
        player_id = cursor.fetchone()["id"]

        return Player(name, number, team_id, player_id)

    def get_team_players(self, team_id: int):
        cursor = self._connection.cursor()

        cursor.execute(
            "SELECT id, name, number FROM players WHERE team_id = ?",
            (team_id,)
        )

        return [Player(row["name"], row["number"], team_id, row["id"])
                for row in cursor.fetchall()]
