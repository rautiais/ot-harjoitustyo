from tkinter import ttk, constants, StringVar, font


class LoggedInView:
    """Class for logged in view
    """

    def __init__(self, root, user_service, team_service, handle_logout, handle_team_view):
        self._root = root
        self._user_service = user_service
        self._team_service = team_service
        self._handle_logout = handle_logout
        self._handle_team_view = handle_team_view
        self._frame = None
        self._team_name_entry = None
        self._error_variable = None
        self._error_label = None
        self._initialize()

    def pack(self):
        """Display the frame"""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroy the frame"""
        self._frame.destroy()

    def _logout_handler(self):
        """Handle logout button click
        """
        self._user_service.logout()
        self._handle_logout()

    def _create_team_handler(self):
        """Handle create team button click
        """
        team_name = self._team_name_entry.get()

        if self._team_service.create_team(team_name):
            self._team_name_entry.delete(0, constants.END)
            self._show_teams()
        else:
            self._error_variable.set("Team creation failed")

    def _handle_team_click(self, team):
        """Handle team button click

        Args:
            team: Team object
        """
        self._handle_team_view(team)
        print(f"Team {team.name} clicked")

    def _show_teams(self):
        """Display the teams of the user
        """
        for widget in self._frame.grid_slaves():
            if isinstance(widget, ttk.Label) and widget.grid_info()["row"] >= 6:
                widget.destroy()

        teams = self._team_service.get_user_teams()
        row = 6

        for team in teams:
            team_frame = ttk.Frame(self._frame)
            team_frame.grid(row=row, column=0, columnspan=2,
                            sticky=constants.W, pady=2, padx=5)

            team_button = ttk.Button(
                master=team_frame,
                text=team.name,
                command=lambda t=team: self._handle_team_click(t)
            )
            team_button.pack(fill=constants.X)
            row += 1

    def _initialize(self):
        """Initialize the view
        """
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)

        user = self._user_service.get_current_user()
        welcome_text = f"Welcome {user.username}!"

        heading_label = ttk.Label(
            master=self._frame,
            text=welcome_text,
            font=font.Font(weight="bold")
        )

        team_name_label = ttk.Label(master=self._frame, text="Team name")
        self._team_name_entry = ttk.Entry(master=self._frame)

        create_team_button = ttk.Button(
            master=self._frame,
            text="Create team",
            command=self._create_team_handler
        )

        logout_button = ttk.Button(
            master=self._frame,
            text="Logout",
            command=self._logout_handler
        )

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='red'
        )

        heading2_label = ttk.Label(
            master=self._frame,
            text="Your teams:",
            font=font.Font(weight="bold")
        )

        heading_label.grid(row=0, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        team_name_label.grid(row=1, column=0, padx=5, pady=5)
        self._team_name_entry.grid(row=1, column=1, sticky=(
            constants.E, constants.W), padx=5, pady=5)
        create_team_button.grid(row=2, column=0, columnspan=2, sticky=(
            constants.E, constants.W), padx=5, pady=5)
        logout_button.grid(row=3, column=0, columnspan=2, sticky=(
            constants.E, constants.W), padx=5, pady=5)
        self._error_label.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
        heading2_label.grid(row=5, column=0, columnspan=2,
                            sticky=constants.W, padx=5, pady=5)

        self._show_teams()
