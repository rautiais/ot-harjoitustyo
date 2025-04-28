from tkinter import Tk
from ui.login_view import LoginView
from ui.registration_view import RegistrationView
from ui.logged_in_view import LoggedInView
from services.user_service import UserService
from services.team_service import TeamService
from ui.team_view import TeamView
from ui.game_view import GameView


class UI:
    """Class for user interface"""

    def __init__(self, root):
        """
        Initializes the UI with the root window.
        Args:
            root (Tk): The root window of the application.
        """
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
        """"Callback method for switching back to login view when logout is successful"""
        self._show_login_view()

    def _handle_team_view(self, team):
        """Callback method for switching to team view
        Args:
            team: The team object to be displayed in the team view.
        """
        self._show_team_view(team)

    def _handle_game_view(self, game, team):
        """Callback method for switching to game view"""
        self._show_game_view(game, team)

    def _show_team_view(self, team):
        """Shows the team view for a specific team
        Args:
            team: The team object to be displayed in the team view.
        """
        self._hide_current_view()
        self._current_view = TeamView(
            self._root,
            team,
            self._team_service,
            self._handle_back_to_team,
            self._handle_game_view
        )
        self._current_view.pack()

    def _handle_back_to_team(self, team):
        """Callback method for returning to the team view"""
        self._show_team_view(team)

    def _show_game_view(self, game, team):
        """Shows the game view for a specific game"""
        self._hide_current_view()
        self._current_view = GameView(
            self._root,
            game,
            team,
            self._team_service,
            lambda: self._handle_back_to_team(team)  # Changed this line
        )
        self._current_view.pack()

    def _show_login_view(self):
        """Hides current view. Creates new login view and passes the registration handle"""
        self._hide_current_view()
        self._current_view = LoginView(
            self._root,
            self._handle_register,
            self._handle_logged_in,
            self._user_service
        )
        self._current_view.pack()

    def _show_register_view(self):
        """Hides the current view. Creates new register view and passes the login handler"""
        self._hide_current_view()
        self._current_view = RegistrationView(
            self._root,
            self._handle_login
        )
        self._current_view.pack()

    def _show_logged_in_view(self):
        """Shows the logged in view"""
        self._hide_current_view()
        self._current_view = LoggedInView(
            self._root,
            self._user_service,
            self._team_service,
            self._handle_logout,
            self._handle_team_view
        )
        self._current_view.pack()

    def start(self):
        """Shows the login view when the application starts"""
        self._show_login_view()
