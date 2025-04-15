from repositories.team_repository import TeamRepository


class TeamService:
    def __init__(self, user_service):
        self._team_repository = TeamRepository()
        self._user_service = user_service

    def create_team(self, team_name: str):
        if len(team_name) < 2:
            return False

        current_user = self._user_service.get_current_user()
        if not current_user:
            return False

        self._team_repository.create_team(team_name, current_user.id)
        return True

    def get_user_teams(self):
        current_user = self._user_service.get_current_user()
        if not current_user:
            return []

        return self._team_repository.get_user_teams(current_user.id)
