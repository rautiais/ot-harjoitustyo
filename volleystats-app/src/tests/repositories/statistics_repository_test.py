import unittest
from repositories.statistics_repository import StatisticsRepository
from repositories.game_repository import GameRepository
from repositories.team_repository import TeamRepository
from repositories.user_repository import UserRepository
from repositories.player_repository import PlayerRepository
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestStatisticsRepository(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.statistics_repository = StatisticsRepository()
        self.game_repository = GameRepository()
        self.team_repository = TeamRepository()
        self.user_repository = UserRepository()
        self.player_repository = PlayerRepository()

        self.test_user = self.user_repository.create_user("Paavo", "Kissa123")
        self.test_team = self.team_repository.create_team(
            "VolleyStars", self.test_user.id)
        self.test_player = self.player_repository.create_player(
            "Paavo", 10, self.test_team.team_id)
        self.test_game = self.game_repository.create_game(
            self.test_team.team_id)

    def tearDown(self):
        close_connection()

    def test_add_pass_stat_succeeds(self):
        """Test that adding a pass stat works"""
        self.statistics_repository.add_pass_stat(
            self.test_game.id, self.test_player.id, 3)
        stats = self.statistics_repository.get_pass_stats_for_game(
            self.test_game.id)
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0][1], 3)

    def test_add_serve_stat(self):
        """Test that adding a serve stat works"""
        self.statistics_repository.add_serve_stat(
            self.test_game.id, self.test_player.id, 3)
        stats = self.statistics_repository.get_game_serve_statistics(
            self.test_game.id)
        self.assertEqual(len(stats), 1)
        self.assertEqual(stats[0][1], 3)

    def test_get_player_pass_stats(self):
        """Test getting pass statistics for a player"""
        self.statistics_repository.add_pass_stat(
            self.test_game.id, self.test_player.id, 3)
        self.statistics_repository.add_pass_stat(
            self.test_game.id, self.test_player.id, 2)
        stats = self.statistics_repository.get_player_pass_stats_for_game(
            self.test_game.id, self.test_player.id)
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0][0], 3)
        self.assertEqual(stats[1][0], 2)

    def test_get_player_serve_stats(self):
        """Test getting serve statistics for a player"""
        self.statistics_repository.add_serve_stat(
            self.test_game.id, self.test_player.id, 3)
        self.statistics_repository.add_serve_stat(
            self.test_game.id, self.test_player.id, 2)
        stats = self.statistics_repository.get_player_serve_stats_for_game(
            self.test_game.id, self.test_player.id)
        self.assertEqual(len(stats), 2)
        self.assertEqual(stats[0][0], 3)
        self.assertEqual(stats[1][0], 2)
