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
