from repositories.user_repository import UserRepository


class UserService:
    def __init__(self):
        self._user_repository = UserRepository()
        self._user = None

    def login(self, username: str, password: str):
        user = self._user_repository.find_by_username(username)

        if not user or user.password != password:
            return False

        self._user = user
        return True

    def logout(self):
        self._user = None

    def create_user(self, username: str, password: str):
        if len(username) < 3 or len(password) < 8:
            return False

        user = self._user_repository.create_user(username, password)
        return user is not None

    def get_current_user(self):
        return self._user
