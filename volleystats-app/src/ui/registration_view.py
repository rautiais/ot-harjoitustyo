from tkinter import ttk, constants, StringVar
from services.user_service import UserService

class RegisterView:
    def __init__(self, root, handle_login_view):
        self.root = root
        self.handle_login_view = handle_login_view
        self.user_service = UserService()
        self.frame = None
        self.username_entry = None
        self.password_entry = None
    
    def pack(self):
        self.frame(fill=constants.X)

    def destroy(self):
        self.frame.destroy()

    def register_handler(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.user_service.create_user(username, password):
            self.handle_login_view()
        else:
            pass

