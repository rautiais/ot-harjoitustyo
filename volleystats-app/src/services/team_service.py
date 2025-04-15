import sqlite3
from repositories.team_repository import TeamRepository
from repositories.player_repository import PlayerRepository


class TeamService:
    def __init__(self, user_service):
        self._team_repository = TeamRepository()
        self._player_repository = PlayerRepository()
        self._user_service = user_service

    def create_team(self, team_name: str):
        if len(team_name) < 2:
            return False

        current_user = self._user_service.get_current_user()
        if not current_user:
            return False

        self._team_repository.create_team(team_name, current_user.id)
        return True

    def create_player(self, team_id: int, name: str, number: int):
        if len(name) < 2 or number < 0:
            return False

        try:
            self._player_repository.create_player(name, number, team_id)
            return True
        except sqlite3.Error:
            return False

    def get_user_teams(self):
        current_user = self._user_service.get_current_user()
        if not current_user:
            return []

        return self._team_repository.get_user_teams(current_user.id)

    def get_team_players(self, team_id: int):
        return self._player_repository.get_team_players(team_id)
