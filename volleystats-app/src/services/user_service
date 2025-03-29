from repositories.user_repository import UserRepository

class UserService:
    def __init__(self):
        self.user_repository = UserRepository()

    def create_user(self, username: str, password: str):
        if len(username) < 3 or len(password) < 8:
            return False
        
        user = self.user_repository.create_user(username, password)
        return user is not None
    
    def login(self, username: str, password: str):
        user = self.user_repository.find_user(username)
        if not user or user.password != password:
            return False
        return True