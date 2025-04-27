import unittest
from datetime import datetime
from repositories.game_repository import GameRepository
from repositories.team_repository import TeamRepository
from repositories.user_repository import UserRepository
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestGameRepository(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.game_repository = GameRepository()
        self.team_repository = TeamRepository()
        self.user_repository = UserRepository()
        # Create test user and team first
        self.test_user = self.user_repository.create_user("Paavo", "Kissa123")
        self.test_team = self.team_repository.create_team(
            "VolleyStars", self.test_user.id)

    def tearDown(self):
        close_connection()

    def test_create_game(self):
        """Test that game can be created"""
        game = self.game_repository.create_game(self.test_team.team_id)
        self.assertEqual(game.team_id, self.test_team.team_id)
        self.assertIsInstance(game.date, datetime)

    def test_get_team_games_when_no_games(self):
        """Test that empty list is returned when no games exist"""
        games = self.game_repository.get_team_games(self.test_team.team_id)
        self.assertEqual(len(games), 0)

    def test_get_team_games_returns_correct_games(self):
        """Test that correct games are returned"""
        game1 = self.game_repository.create_game(self.test_team.team_id)
        game2 = self.game_repository.create_game(self.test_team.team_id)

        games = self.game_repository.get_team_games(self.test_team.team_id)
        self.assertEqual(len(games), 2)
        self.assertEqual(games[0].id, game2.id)
        self.assertEqual(games[1].id, game1.id)
