class User:
    """
    Represents a user in the system.
    """

    def __init__(self, username: str, password: str, user_id: int = None):
        self.username = username
        self.password = password
        self.id = user_id
