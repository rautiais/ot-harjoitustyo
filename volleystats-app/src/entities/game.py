from datetime import datetime


class Game:
    """Class representing a volleyball game"""

    def __init__(self, team_id: int, date: datetime = None, game_id: int = None):
        """Initialize a new game

        Args:
            team_id: ID of the team playing
            date: Date of the game, defaults to current time
            game_id: ID of the game in database, defaults to None for new games
        """
        self.team_id = team_id
        self.date = date or datetime.now()
        self.id = game_id
