import unittest
from services.team_service import TeamService
from services.user_service import UserService
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestTeamService(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.user_service = UserService()
        self.team_service = TeamService(self.user_service)
        # Create and login a test user
        self.user_service.create_user("Paavo", "Kissa123")
        self.user_service.login("Paavo", "Kissa123")

    def tearDown(self):
        close_connection()

    def test_create_team_with_valid_name(self):
        """Test that creating a team with a valid name works"""
        result = self.team_service.create_team("VolleyStars")
        self.assertTrue(result)

    def test_create_team_with_too_short_name(self):
        """Test that creating a team with a too short name doesn't work"""
        result = self.team_service.create_team("V")
        self.assertFalse(result)

    def test_create_team_when_not_logged_in(self):
        """Test that creating a team when not logged in doesn't work"""
        self.user_service.logout()
        result = self.team_service.create_team("VolleyStars")
        self.assertFalse(result)

    def test_get_user_teams(self):
        """Test that getting a user's teams works"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_team("VolleySuns")

        teams = self.team_service.get_user_teams()
        self.assertEqual(len(teams), 2)
        self.assertEqual(teams[0].name, "VolleyStars")
        self.assertEqual(teams[1].name, "VolleySuns")

    def test_get_teams_when_not_logged_in(self):
        """Test that getting teams when not logged in doesn't work"""
        self.user_service.logout()
        teams = self.team_service.get_user_teams()
        self.assertEqual(len(teams), 0)

    def test_create_game_succeeds(self):
        """Test that game creation works"""
        self.team_service.create_team("VolleyStars")
        result = self.team_service.create_game(1)
        self.assertTrue(result)

    def test_get_team_games_returns_empty_list_when_no_games(self):
        """Test that empty list is returned when team has no games"""
        self.team_service.create_team("VolleyStars")
        games = self.team_service.get_team_games(1)
        self.assertEqual(len(games), 0)

    def test_get_team_games_returns_all_games(self):
        """Test that all team games are returned"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_game(1)
        self.team_service.create_game(1)

        games = self.team_service.get_team_games(1)
        self.assertEqual(len(games), 2)

    def test_get_player_pass_average(self):
        """Test that getting a player's pass average works"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_player(1, "Salde", 13)
        self.team_service.create_game(1)
        self.team_service.add_pass_stat(1, 1, 3)
        self.team_service.add_pass_stat(1, 1, 1)

        average = self.team_service.get_player_pass_average(1, 1)
        self.assertEqual(average, 2.0)

    def test_get_player_serve_average(self):
        """Test that getting a player's serve average works"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_player(1, "Salde", 13)
        self.team_service.create_game(1)
        self.team_service.add_serve_stat(1, 1, 3)
        self.team_service.add_serve_stat(1, 1, 1)

        average = self.team_service.get_player_serve_average(1, 1)
        self.assertEqual(average, 2.0)

    def test_get_team_pass_average(self):
        """Test that getting a team's pass average works"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_player(1, "Salde", 13)
        self.team_service.create_player(1, "Kalle", 8)
        self.team_service.create_game(1)
        self.team_service.add_pass_stat(1, 1, 3)
        self.team_service.add_pass_stat(1, 2, 1)

        average = self.team_service.get_pass_average(1)
        self.assertEqual(average, 2.0)

    def test_get_team_serve_average(self):
        """Test that getting a team's serve average works"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_player(1, "Salde", 13)
        self.team_service.create_player(1, "Kalle", 8)
        self.team_service.create_game(1)
        self.team_service.add_serve_stat(1, 1, 3)
        self.team_service.add_serve_stat(1, 2, 1)

        average = self.team_service.get_team_serve_average(1)
        self.assertEqual(average, 2.0)

    def test_no_pass_stats(self):
        """Test that average is 0.0 when no pass stats exist"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_game(1)
        average = self.team_service.get_pass_average(1)
        self.assertEqual(average, 0.0)

    def test_no_serve_stats(self):
        """Test that average is 0.0 when no serve stats exist"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_game(1)
        average = self.team_service.get_team_serve_average(1)
        self.assertEqual(average, 0.0)

    def test_no_player_pass_stats(self):
        """Test that average is 0.0 when no player pass stats exist"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_player(1, "Salde", 13)
        self.team_service.create_game(1)
        average = self.team_service.get_player_pass_average(1, 1)
        self.assertEqual(average, 0.0)

    def test_no_player_serve_stats(self):
        """Test that average is 0.0 when no player serve stats exist"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_player(1, "Salde", 13)
        self.team_service.create_game(1)
        average = self.team_service.get_player_serve_average(1, 1)
        self.assertEqual(average, 0.0)

    def test_end_game_succeeds(self):
        """Test that ending a game works"""
        self.team_service.create_team("VolleyStars")
        self.team_service.create_game(1)
        result = self.team_service.end_game(1)
        self.assertTrue(result)

        games = self.team_service.get_team_games(1)
        self.assertEqual(len(games), 1)
        self.assertFalse(games[0].is_ongoing())
