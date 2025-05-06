from datetime import datetime


class Game:
    """Class representing a volleyball game"""

    def __init__(self, team_id: int, date: datetime = None, game_id: int = None,
                 status: str = "ongoing"):
        """Initialize a new game

        Args:
            team_id: ID of the team playing
            date: Date of the game, defaults to current time
            game_id: ID of the game in database, defaults to None for new games
            status: Status of the game, defaults to "ongoing"
        """
        self.team_id = team_id
        self.date = date or datetime.now()
        self.id = game_id
        self.status = status

    def is_ongoing(self):
        """Check if the game has ended

        Returns:
            bool: True if game status is 'ongoing'
        """
        return self.status == "ongoing"
