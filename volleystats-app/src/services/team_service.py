import sqlite3
from repositories.team_repository import TeamRepository
from repositories.player_repository import PlayerRepository
from repositories.game_repository import GameRepository
from repositories.statistics_repository import StatisticsRepository


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
        self._game_repository = GameRepository()
        self._statistics_repository = StatisticsRepository()
        self._user_service = user_service

    def create_team(self, team_name: str):
        """
        Creates a new team with the given name.

        Args:
            team_name (str): The name of the team to be created.

        Returns:
            bool: True if the team was created successfully.
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
            bool: True if the player was created successfully.
            False: if the player name is invalid, the number is negative, 
            or the user is not logged in.
        """
        if len(name) < 2 or number < 0:
            return False

        try:
            self._player_repository.create_player(name, number, team_id)
            return True
        except sqlite3.Error:
            return False

    def create_game(self, team_id: int) -> bool:
        """Create a new game for a team

        Args:
            team_id: ID of the team

        Returns:
            bool: True if game was created successfully
        """
        try:
            self._game_repository.create_game(team_id)
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

    def get_team_games(self, team_id: int):
        """Get all games for a team

        Args:
            team_id: ID of the team

        Returns:
            list: List of Game objects
        """
        return self._game_repository.get_team_games(team_id)

    def add_pass_stat(self, game_id: int, player_id: int, score: int) -> bool:
        """Add a pass statistic for a player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player
            score: Pass score (0-3)

        Returns:
            bool: True if statistic was added successfully, False otherwise
        """
        try:
            self._statistics_repository.add_pass_stat(
                game_id, player_id, score)
            return True
        except sqlite3.Error:
            return False

    def get_pass_average(self, game_id: int) -> float:
        """Calculate average pass score for a game

        Args:
            game_id: ID of the game

        Returns:
            float: Average pass score, or 0.0 if no passes
        """
        try:
            stats = self._statistics_repository.get_pass_stats_for_game(
                game_id)
            if not stats:
                return 0.0
            total_score = sum(score for _, score in stats)
            return round(total_score / len(stats), 2)
        except sqlite3.Error:
            return 0.0

    def get_player_pass_average(self, game_id: int, player_id: int) -> float:
        """Calculate average pass score for a player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player

        Returns:
            float: Player's average pass score for the game, or 0.0 if no passes
        """
        try:
            stats = self._statistics_repository.get_player_pass_stats_for_game(
                game_id, player_id)
            if not stats:
                return 0.0
            total_score = sum(score[0] for score in stats)
            return round(total_score / len(stats), 2)
        except sqlite3.Error:
            return 0.0

    def add_serve_stat(self, game_id: int, player_id: int, score: int) -> bool:
        """Add a serve statistic for a player

        Args:
            game_id: ID of the game
            player_id: ID of the player
            score: Serve score (0-3)

        Returns:
            bool: True if statistic was added successfully
        """
        try:
            self._statistics_repository.add_serve_stat(game_id, player_id, score)
            return True
        except sqlite3.Error:
            return False

    def get_player_serve_average(self, game_id: int, player_id: int) -> float:
        """Calculate average serve score for a player in a game

        Args:
            game_id: ID of the game
            player_id: ID of the player

        Returns:
            float: Player's average serve score for the game, or 0.0 if no serves
        """
        try:
            stats = self._statistics_repository.get_player_serve_stats_for_game(game_id, player_id)
            if not stats:
                return 0.0
            total_score = sum(score[0] for score in stats)
            return round(total_score / len(stats), 2)
        except sqlite3.Error:
            return 0.0

    def get_team_serve_average(self, game_id: int) -> float:
        """Calculate team's average serve score for a game

        Args:
            game_id: ID of the game

        Returns:
            float: Team's average serve score, or 0.0 if no serves
        """
        try:
            stats = self._statistics_repository.get_game_serve_statistics(game_id)
            if not stats:
                return 0.0
            total_score = sum(score for _, score in stats)
            return round(total_score / len(stats), 2)
        except sqlite3.Error:
            return 0.0

    def end_game(self, game_id: int) -> bool:
        """End a game

        Args:
            game_id: ID of the game to end

        Returns:
            bool: True if game was ended successfully
        """
        try:
            self._game_repository.update_game_status(game_id, "ended")
            return True
        except sqlite3.Error:
            return False
