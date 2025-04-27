class Player:
    """
    Represents a player in a volleyball team.
    """

    def __init__(self, name: str, number: int, team_id: int, player_id: int = None):
        self.name = name
        self.number = number
        self.team_id = team_id
        self.id = player_id
