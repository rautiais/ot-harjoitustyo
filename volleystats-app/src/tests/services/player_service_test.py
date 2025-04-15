import unittest
from services.team_service import TeamService
from services.user_service import UserService
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestPlayerService(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.user_service = UserService()
        self.team_service = TeamService(self.user_service)
        self.user_service.create_user("Paavo", "Kissa123")
        self.user_service.login("Paavo", "Kissa123")
        self.team_service.create_team("VolleyStars")

    def tearDown(self):
        close_connection()

    def test_create_player_with_valid_info(self):
        """Test that player can be created with valid info"""
        result = self.team_service.create_player(1, "Maija Meikäläinen", 10)
        self.assertTrue(result)

    def test_create_player_with_too_short_name(self):
        """Test that player creation fails with too short name"""
        result = self.team_service.create_player(1, "J", 10)
        self.assertFalse(result)

    def test_create_player_with_negative_number(self):
        """Test that player creation fails with negative number"""
        result = self.team_service.create_player(1, "Maija Meikäläinen", -1)
        self.assertFalse(result)

    def test_get_team_players(self):
        """Test that getting team players works"""
        self.team_service.create_player(1, "Maija Meikäläinen", 10)
        self.team_service.create_player(1, "Taija Teikäläinen", 7)

        players = self.team_service.get_team_players(1)
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, "Maija Meikäläinen")
        self.assertEqual(players[1].name, "Taija Teikäläinen")

    def test_get_team_players_when_none(self):
        """Test that empty list is returned when team has no players"""
        players = self.team_service.get_team_players(1)
        self.assertEqual(len(players), 0)
