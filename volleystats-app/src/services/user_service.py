from repositories.user_repository import UserRepository


class UserService:
    """
    Service class for managing user authentication and user-related operations.
    """

    def __init__(self):
        """
        Initializes the UserService with a user repository.
        """
        self._user_repository = UserRepository()
        self._user = None

    def login(self, username: str, password: str):
        """
        Authenticates a user with the given username and password.

        Args:
            username (str): Username of the user.
            password (str): Password of the user.

        Returns:
            True: if the user is authenticated successfully.
            False: if the username or password is incorrect.
        """
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            return False

        self._user = user
        return True

    def logout(self):
        """
        Logs out the current user.
        """
        self._user = None

    def create_user(self, username: str, password: str):
        """
        Creates a new user with the given username and password.

        Args:
            username (str): Username of the new user.
            password (str): Password of the new user.

        Returns:
            False: if the username or password is invalid.
            User: if the user was created successfully.
        """
        if len(username) < 3 or len(password) < 8:
            return False

        user = self._user_repository.create_user(username, password)
        return user is not None

    def get_current_user(self):
        """
        Returns the currently logged-in user.
        """
        return self._user
