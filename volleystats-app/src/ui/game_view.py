from tkinter import ttk, constants, StringVar, font


class GameView:
    def __init__(self, root, game, team, team_service, handle_back):
        """Initialize GameView

        Args:
            root: Tkinter root
            game: Game object to display
            team: Team object
            team_service: TeamService instance
            handle_back: Callback for returning to team view
        """
        self._root = root
        self._game = game
        self._team = team
        self._team_service = team_service
        self._handle_back = handle_back
        self._frame = None
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
        self._frame = ttk.Frame(master=self._root)
        self._error_variable = StringVar(self._frame)

        heading_label = ttk.Label(
            master=self._frame,
            text=f"Game on {self._game.date.strftime('%Y-%m-%d %H:%M')}",
            font=font.Font(weight="bold")
        )

        roster_label = ttk.Label(
            master=self._frame,
            text="Team Roster:",
            font=font.Font(weight="bold")
        )

        back_button = ttk.Button(
            master=self._frame,
            text="Back to team",
            command=self._handle_back
        )

        self._error_label = ttk.Label(
            master=self._frame,
            textvariable=self._error_variable,
            foreground='red'
        )

        heading_label.grid(row=0, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        roster_label.grid(row=1, column=0, columnspan=2,
                          sticky=constants.W, padx=5, pady=5)

        self._show_players()

        back_button.grid(row=20, column=0, columnspan=2,
                         sticky=(constants.E, constants.W), padx=5, pady=5)
        self._error_label.grid(row=21, column=0, columnspan=2, padx=5, pady=5)

    def _show_players(self):
        """Display team roster"""
        players = self._team_service.get_team_players(self._team.team_id)
        row = 2

        if not players:
            no_players_label = ttk.Label(
                master=self._frame,
                text="No players in roster"
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
