from tkinter import ttk, constants, StringVar
from services.user_service import UserService

class RegisterView:
    def __init__(self, root, handle_login_view):
        self._root = root
        self._handle_login_view = handle_login_view
        self._user_service = UserService()
        self._frame = None
        self._username_entry = None
        self._password_entry = None
    
    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def register_handler(self):
        username = self._username_entry.get()
        password = self._password_entry.get()

        if self._user_service.create_user(username, password):
            self._handle_login_view()
        else:
            pass

