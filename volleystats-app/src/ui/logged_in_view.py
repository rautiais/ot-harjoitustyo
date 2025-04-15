from tkinter import ttk, constants, StringVar, font


class LoggedInView:
    def __init__(self, root, user_service, team_service, handle_logout):
        self._root = root
        self._user_service = user_service
        self._team_service = team_service
        self._handle_logout = handle_logout
        self._frame = None
        self._team_name_entry = None
        self._error_variable = None
        self._error_label = None
        self._initialize()

    def pack(self):
        self._frame.pack(fill=constants.X)

    def destroy(self):
        self._frame.destroy()

    def _logout_handler(self):
        self._user_service.logout()
        self._handle_logout()

    def _create_team_handler(self):
        team_name = self._team_name_entry.get()

        if self._team_service.create_team(team_name):
            self._team_name_entry.delete(0, constants.END)
            self._show_teams()
        else:
            self._error_variable.set("Team creation failed")

    def _show_teams(self):
        # Clear existing team labels
        for widget in self._frame.grid_slaves():
            if isinstance(widget, ttk.Label) and widget.grid_info()["row"] >= 6:
                widget.destroy()

        teams = self._team_service.get_user_teams()
        row = 6

        for team in teams:
            label = ttk.Label(master=self._frame, text=f"{team.name}")
            label.grid(row=row, column=0, columnspan=2, sticky=constants.W, pady=5, padx=5)
            row += 1

    def _initialize(self):
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
