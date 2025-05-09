from tkinter import ttk, constants, StringVar, font


class TeamView:
    """Class for team view
    """

    def __init__(self, root, team, team_service, handle_back, handle_game_view):
        """
        Initializes the team view with the given parameters.

        Args:
            root: root window of the application
            team: team object to be displayed
            team_service: team service for managing team data
            handle_back: handler for going back to the previous view
            handle_game_view: handler for displaying the game view
        """
        self._root = root
        self._team = team
        self._team_service = team_service
        self._handle_back = handle_back
        self._handle_game_view = handle_game_view
        self._frame = None
        self._player_name_entry = None
        self._player_number_entry = None
        self._error_variable = None
        self._error_label = None
        self._initialize()

    def pack(self):
        """Display the frame"""
        self._frame.pack(fill=constants.X)

    def destroy(self):
        """Destroy the frame"""
        self._frame.destroy()

    def _initialize(self):
        """Initialize the team view
        """
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)

        heading_label = ttk.Label(
            master=self._frame,
            text=f"Team: {self._team.name}",
            font=font.Font(weight="bold")
        )

        player_name_label = ttk.Label(
            master=self._frame,
            text="Player name"
        )
        self._player_name_entry = ttk.Entry(master=self._frame)

        player_number_label = ttk.Label(
            master=self._frame,
            text="Jersey number"
        )
        self._player_number_entry = ttk.Entry(master=self._frame)

        add_player_button = ttk.Button(
            master=self._frame,
            text="Add player",
            command=self._add_player_handler
        )

        start_game_button = ttk.Button(
            master=self._frame,
            text="Start new game",
            command=self._start_game_handler
        )

        games_label = ttk.Label(
            master=self._frame,
            text="Games:",
            font=font.Font(weight="bold")
        )

        back_button = ttk.Button(
            master=self._frame,
            text="Back to teams",
            command=self._handle_back
        )

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='red'
        )

        players_label = ttk.Label(
            master=self._frame,
            text="Players:",
            font=font.Font(weight="bold")
        )

        heading_label.grid(row=0, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        player_name_label.grid(row=1, column=0, padx=5, pady=5)
        self._player_name_entry.grid(
            row=1, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        player_number_label.grid(row=2, column=0, padx=5, pady=5)
        self._player_number_entry.grid(
            row=2, column=1, sticky=(constants.E, constants.W), padx=5, pady=5)
        add_player_button.grid(
            row=3, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        players_label.grid(row=4, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        games_label.grid(row=15, column=0, columnspan=2,
                         sticky=constants.W, padx=5, pady=5)
        start_game_button.grid(
            row=16, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        back_button.grid(
            row=30, column=0, columnspan=2, sticky=(constants.E, constants.W), padx=5, pady=5)
        self._error_label.grid(row=31, column=0, columnspan=2, padx=5, pady=5)

        self._show_players()
        self._show_games()

    def _add_player_handler(self):
        """Handle adding a new player to the team
        """
        name = self._player_name_entry.get()
        number = self._player_number_entry.get()

        if not name or not number:
            self._error_variable.set("Name and number required")
            return

        try:
            number = int(number)
        except ValueError:
            self._error_variable.set("Number must be a valid integer")
            return

        if self._team_service.create_player(self._team.team_id, name, number):
            self._player_name_entry.delete(0, constants.END)
            self._player_number_entry.delete(0, constants.END)
            self._error_variable.set("")
            self._show_players()
        else:
            self._error_variable.set("Failed to add player")

    def _show_players(self):
        """Display all players for this team
        """
        for widget in self._frame.grid_slaves():
            if isinstance(widget, ttk.Label) and 5 <= widget.grid_info()["row"] < 15:
                widget.destroy()

        players = self._team_service.get_team_players(self._team.team_id)
        row = 5

        if not players:
            no_players_label = ttk.Label(
                master=self._frame,
                text="No players added yet"
            )
            no_players_label.grid(row=row, column=0, columnspan=2,
                                  sticky=constants.W, padx=5, pady=2)
            return

        for player in players:
            player_label = ttk.Label(
                master=self._frame,
                text=f"#{player.number} {player.name}"
            )
            player_label.grid(row=row, column=0, columnspan=2,
                              sticky=constants.W, padx=5, pady=2)
            row += 1

    def _start_game_handler(self):
        """Handle starting a new game"""
        if self._team_service.create_game(self._team.team_id):
            self._show_games()
        else:
            self._error_variable.set("Failed to start game")

    def _show_games(self):
        """Display all games for this team"""
        for widget in self._frame.grid_slaves():
            if isinstance(widget, ttk.Label) and 17 <= widget.grid_info()["row"] < 30:
                widget.destroy()

        games = self._team_service.get_team_games(self._team.team_id)
        row = 17

        if not games:
            no_games_label = ttk.Label(
                master=self._frame,
                text="No games played yet"
            )
            no_games_label.grid(row=row, column=0, columnspan=2,
                                sticky=constants.W, padx=5, pady=2)
            return

        for game in games:
            game_button = ttk.Button(
                master=self._frame,
                text=f"Game on {game.date.strftime('%Y-%m-%d %H:%M')}",
                command=lambda g=game: self._handle_game_view(g, self._team)
            )
            game_button.grid(row=row, column=0, columnspan=2,
                             sticky=(constants.E, constants.W), padx=5, pady=2)
            row += 1
