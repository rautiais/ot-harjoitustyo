from tkinter import ttk, constants, StringVar, font


class GameView:
    """Class for displaying game information and statistics
    """

    def __init__(self, root, game, team, team_service, handle_back):
        """Initialize GameView

        Args:
            root: Tkinter root
            game: Game object to display
            team: Team object
            team_service: TeamService instance
            handle_back: Callback for returning to the previous view
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
        """Initialize the game view
        """
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
            text="Scoring:",
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

        stats_label = ttk.Label(
            master=self._frame,
            text="Statistics:",
            font=font.Font(weight="bold")
        )

        scoring_info = ttk.Label(
            master=self._frame,
            text=("Pass: 0=Error, 1=Poor, 2=Good, 3=Perfect\n"
                  "Serve: 0=Error, 1=Easy serve, 2=Out of system, 3=Ace")
        )

        self._average_label = ttk.Label(
            master=self._frame,
            text=f"Pass Average: {self._team_service.get_pass_average(self._game.id)}"
        )

        self._serve_average_label = ttk.Label(
            master=self._frame,
            text=f"Serve Average: {self._team_service.get_team_serve_average(self._game.id)}"
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

        self._end_game_button = ttk.Button(
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
        stats_label.grid(row=27, column=0, columnspan=2,
                         sticky=constants.W, padx=5, pady=5)
        self._average_label.grid(row=28, column=0, columnspan=2,
                                 sticky=constants.W, padx=5, pady=2)
        self._serve_average_label.grid(row=29, column=0, columnspan=2,
                                       sticky=constants.W, padx=5, pady=2)
        self._end_game_button.grid(row=30, column=0, columnspan=2,
                                   sticky=(constants.E, constants.W), padx=5, pady=5)
        back_button.grid(row=31, column=0, columnspan=2,
                         sticky=(constants.E, constants.W), padx=5, pady=5)
        self._error_label.grid(row=32, column=0, columnspan=2, padx=5, pady=5)

    def _show_players_with_scoring(self):
        """Display team roster with scoring buttons and statistics"""
        players = self._team_service.get_team_players(self._team.team_id)
        row = 4

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

            # Player info with pass and serve averages
            pass_avg = self._team_service.get_player_pass_average(
                self._game.id, player.id)
            serve_avg = self._team_service.get_player_serve_average(
                self._game.id, player.id)
            player_label = ttk.Label(
                master=player_frame,
                text=f"#{player.number} {player.name} (Pass: {pass_avg} | Serve: {serve_avg})"
            )
            player_label.pack(side=constants.LEFT, padx=5)

            if self._game.is_ongoing():
                # Pass score buttons
                pass_frame = ttk.Frame(player_frame)
                ttk.Label(master=pass_frame, text="Pass:").pack(
                    side=constants.LEFT, padx=2)
                for score in range(4):
                    score_button = ttk.Button(
                        master=pass_frame,
                        text=str(score),
                        command=lambda p=player, s=score: self._add_pass_stat(
                            p, s)
                    )
                    score_button.pack(side=constants.LEFT, padx=2)
                pass_frame.pack(side=constants.LEFT, padx=5)

                # Serve score buttons
                serve_frame = ttk.Frame(player_frame)
                ttk.Label(master=serve_frame, text="Serve:").pack(
                    side=constants.LEFT, padx=2)
                for score in range(4):
                    score_button = ttk.Button(
                        master=serve_frame,
                        text=str(score),
                        command=lambda p=player, s=score: self._add_serve_stat(
                            p, s)
                    )
                    score_button.pack(side=constants.LEFT, padx=2)
                serve_frame.pack(side=constants.LEFT, padx=5)

            player_frame.grid(row=row, column=0, columnspan=2,
                              sticky=constants.W, padx=5, pady=2)
            row += 1

        if self._game.is_ongoing():
            self._end_game_button.grid(row=30, column=0, columnspan=2,
                                       sticky=(constants.E, constants.W), padx=5, pady=5)
        else:
            self._end_game_button.grid_remove()

    def _add_pass_stat(self, player, score):
        """Add a pass statistic for a player"""
        if self._team_service.add_pass_stat(self._game.id, player.id, score):
            team_avg = self._team_service.get_pass_average(self._game.id)
            player_avg = self._team_service.get_player_pass_average(
                self._game.id, player.id)
            self._average_label.configure(
                text=f"Team Pass Average: {team_avg}")
            self._show_players_with_scoring()
            self._error_variable.set(f"Added {score} pass for {player.name}")
        else:
            self._error_variable.set("Failed to add statistic")

    def _add_serve_stat(self, player, score):
        """Add a serve statistic for a player"""
        if self._team_service.add_serve_stat(self._game.id, player.id, score):
            team_serve_avg = self._team_service.get_team_serve_average(
                self._game.id)
            self._serve_average_label.configure(
                text=f"Team Serve Average: {team_serve_avg}")
            self._show_players_with_scoring()
            self._error_variable.set(
                f"Added serve score {score} for {player.name}")
        else:
            self._error_variable.set("Failed to add serve statistic")

    def _end_game_handler(self):
        """Handle ending the game"""
        if self._team_service.end_game(self._game.id):
            self._handle_back()
        else:
            self._error_variable.set("Failed to end game")
