import sqlite3
from repositories.team_repository import TeamRepository
from repositories.player_repository import PlayerRepository


class TeamService:
    """
    Service class for managing teams and players.
    """

    def __init__(self, user_service):
        """
        Initializes the TeamService with a user service.

        Args:
            user_service: An instance of the user service to manage user-related operations.
        """
        self._team_repository = TeamRepository()
        self._player_repository = PlayerRepository()
        self._user_service = user_service

    def create_team(self, team_name: str):
        """
        Creates a new team with the given name.

        Args:
            team_name (str): The name of the team to be created.

        Returns:
            True: if the team was created successfully.
            False: if the team name is invalid or the user is not logged in.
        """
        if len(team_name) < 2:
            return False

        current_user = self._user_service.get_current_user()
        if not current_user:
            return False

        self._team_repository.create_team(team_name, current_user.id)
        return True

    def create_player(self, team_id: int, name: str, number: int):
        """
        Creates a new player for the given team.

        Args:
            team_id (int): The ID of the team to which the player belongs.
            name (str): The name of the player to be created.
            number (int): The number of the player to be created.

        Returns:
            True: if the player was created successfully.
            False: if the player name is invalid, the number is negative, or the user is not logged in.
        """
        if len(name) < 2 or number < 0:
            return False

        try:
            self._player_repository.create_player(name, number, team_id)
            return True
        except sqlite3.Error:
            return False

    def get_user_teams(self):
        """
        Retrieves the teams associated with the current user.

        Returns:
            List: A list of teams associated with the current user.
            Empty list: if the user is not logged in.
        """
        current_user = self._user_service.get_current_user()
        if not current_user:
            return []

        return self._team_repository.get_user_teams(current_user.id)

    def get_team_players(self, team_id: int):
        """
        Retrieves the players associated with a specific team.

        Args:
            team_id (int): The ID of the team for which to retrieve players.

        Returns:
            List: A list of players associated with the specified team.
        """
        return self._player_repository.get_team_players(team_id)
