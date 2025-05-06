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

        # Create labels
        heading_label = ttk.Label(
            master=self._frame,
            text=f"Game on {self._game.date.strftime('%Y-%m-%d %H:%M')}",
            font=font.Font(weight="bold")
        )

        scoring_label = ttk.Label(
            master=self._frame,
            text="Pass Scoring:",
            font=font.Font(weight="bold")
        )

        scoring_info = ttk.Label(
            master=self._frame,
            text="0 = Error, 1 = Poor, 2 = Good, 3 = Perfect"
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

        end_game_button = ttk.Button(
            master=self._frame,
            text="End Game",
            command=self._end_game_handler
        )

        # Layout
        heading_label.grid(row=0, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        scoring_label.grid(row=1, column=0, columnspan=2,
                           sticky=constants.W, padx=5, pady=5)
        scoring_info.grid(row=2, column=0, columnspan=2,
                          sticky=constants.W, padx=5, pady=2)
        roster_label.grid(row=3, column=0, columnspan=2,
                          sticky=constants.W, padx=5, pady=5)

        self._show_players_with_scoring()

        end_game_button.grid(row=29, column=0, columnspan=2,
                             sticky=(constants.E, constants.W), padx=5, pady=5)
        back_button.grid(row=30, column=0, columnspan=2,
                         sticky=(constants.E, constants.W), padx=5, pady=5)
        self._error_label.grid(row=31, column=0, columnspan=2, padx=5, pady=5)

    def _show_players_with_scoring(self):
        """Display team roster with scoring buttons"""
        players = self._team_service.get_team_players(self._team.team_id)
        row = 4  # Start after roster label

        if not players:
            no_players_label = ttk.Label(
                master=self._frame,
                text="No players in roster"
            )
            no_players_label.grid(row=row, column=0, columnspan=2,
                                  sticky=constants.W, padx=5, pady=2)
            return

        for player in players:
            player_frame = ttk.Frame(self._frame)
            player_label = ttk.Label(
                master=player_frame,
                text=f"#{player.number} {player.name}"
            )
            player_label.pack(side=constants.LEFT, padx=5)

            for score in range(4):
                score_button = ttk.Button(
                    master=player_frame,
                    text=str(score),
                    command=lambda p=player, s=score: self._add_pass_stat(p, s)
                )
                score_button.pack(side=constants.LEFT, padx=2)

            player_frame.grid(row=row, column=0, columnspan=2,
                              sticky=constants.W, padx=5, pady=2)
            row += 1

    def _add_pass_stat(self, player, score):
        """Add a pass statistic for a player"""
        if self._team_service.add_pass_stat(self._game.id, player.id, score):
            self._error_variable.set(f"Added {score} pass for {player.name}")
        else:
            self._error_variable.set("Failed to add statistic")

    def _end_game_handler(self):
        """Handle ending the game"""
        if self._team_service.end_game(self._game.id):
            self._handle_back()  # Return to team view
        else:
            self._error_variable.set("Failed to end game")
