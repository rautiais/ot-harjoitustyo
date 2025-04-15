from tkinter import Tk
from ui.login_view import LoginView
from ui.registration_view import RegistrationView
from ui.logged_in_view import LoggedInView
from services.user_service import UserService
from services.team_service import TeamService


class UI:
    """Class for user interface"""

    def __init__(self, root):
        """Entity is created to handle all ui functionality. Current view keeps track of which view is displayed currently"""
        self._root = root
        self._current_view = None
        self._user_service = UserService()
        self._team_service = TeamService(self._user_service)

    def _hide_current_view(self):
        """Hides current window if it exists"""
        if self._current_view:
            self._current_view.destroy()

    def _handle_register(self):
        """Callback method for switching to registration view"""
        self._show_register_view()

    def _handle_login(self):
        """Callback method for switching back to login view"""
        self._show_login_view()

    def _handle_logged_in(self):
        """Callback method for switching to logged in view when login is successful"""
        self._show_logged_in_view()

    def _handle_logout(self):
        """"""""
        self._show_login_view()

    def _show_login_view(self):
        """Hides the current view"""
        self._hide_current_view()
        """Creates new login view and passes the registration handle"""
        self._current_view = LoginView(
            self._root,
            self._handle_register,
            self._handle_logged_in,
            self._user_service
        )
        self._current_view.pack()

    def _show_register_view(self):
        """Hides the current view"""
        self._hide_current_view()
        """Creates new register view and passes the login handler"""
        self._current_view = RegistrationView(
            self._root,
            self._handle_login
        )
        self._current_view.pack()

    def _show_logged_in_view(self):
        """Hides the current view"""
        self._hide_current_view()
        self._current_view = LoggedInView(
            self._root,
            self._user_service,
            self._team_service,
            self._handle_logout
        )
        self._current_view.pack()

    def start(self):
        """Shows the login view when the application starts"""
        self._show_login_view()
