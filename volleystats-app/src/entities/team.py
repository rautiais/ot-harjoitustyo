class Team:
    """
    Represents a team in the system.
    """

    def __init__(self, name: str, user_id: int, team_id: int = None):
        self.name = name
        self.user_id = user_id
        self.team_id = team_id
