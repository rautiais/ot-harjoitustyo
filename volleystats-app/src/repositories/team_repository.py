from entities.team import Team
from database_connection import get_database_connection


class TeamRepository:
    """
    Repository for managing team data in the database.
    """

    def __init__(self):
        """Initializes the TeamRepository with a database connection."""
        self._connection = get_database_connection()

    def create_team(self, name: str, user_id: int):
        """
        Creates a new team in the database.

        Args:
            name (str): Team name.
            user_id (int): ID of the user who created the team.

        Returns:
            Class: Team object representing the created team.
        """
        cursor = self._connection.cursor()

        cursor.execute('''
            INSERT INTO teams (name, user_id)
            VALUES (?, ?);
        ''', (name, user_id))
        self._connection.commit()

        cursor.execute('''
            SELECT id FROM teams WHERE name = ? AND user_id = ?;
        ''', (name, user_id))
        team_id = cursor.fetchone()["id"]

        return Team(name, user_id, team_id)

    def get_user_teams(self, user_id: int):
        """
        Retrieves all teams for a given user from the database.

        Args:
            user_id (int): ID of the user.

        Returns:
            List: A list of Team objects belonging to the user.
        """
        cursor = self._connection.cursor()

        cursor.execute('''
            SELECT id, name FROM teams WHERE user_id = ?;
        ''', (user_id,))

        return [Team(row["name"], user_id, row["id"]) for row in cursor.fetchall()]
