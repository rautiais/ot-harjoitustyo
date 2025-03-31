from entities.user import User

class UserRepository:
    def __init__(self):
        self.users = {}

    def create_user(self, username: str, password: str):
        if self.find_by_username(username):
            return None
        user = User(username, password)
        self.users[username] = user
        return user
    
    def find_by_username(self, username: str):
        return self.users.get(username)