from entities.user import User

class UserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, username: str, password: str):
        if username in self.users:
            return None
        user = User(username, password)
        self.users[username] = user
        return user
    
    def find_user(self, username: str):
        return self.users.get(username)