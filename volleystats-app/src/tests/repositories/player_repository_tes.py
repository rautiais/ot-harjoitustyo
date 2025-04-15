import unittest
from repositories.player_repository import PlayerRepository
from repositories.team_repository import TeamRepository
from repositories.user_repository import UserRepository
from initialize_database import initialize_database
from database_connection import set_database_path, close_connection
from config import TEST_DATABASE_FILE_PATH


class TestPlayerRepository(unittest.TestCase):
    def setUp(self):
        set_database_path(TEST_DATABASE_FILE_PATH)
        initialize_database()
        self.player_repository = PlayerRepository()
        self.team_repository = TeamRepository()
        self.user_repository = UserRepository()
        self.test_user = self.user_repository.create_user("Paavo", "Kissa123")
        self.test_team = self.team_repository.create_team(
            "VolleyStars", self.test_user.id)

    def tearDown(self):
        close_connection()

    def test_create_player(self):
        """Test that creating a player works"""
        player = self.player_repository.create_player(
            "Maija Meikäläinen", 10, self.test_team.team_id)
        self.assertEqual(player.name, "Maija Meikäläinen")
        self.assertEqual(player.number, 10)
        self.assertEqual(player.team_id, self.test_team.team_id)

    def test_get_team_players(self):
        """Test that getting team's players works"""
        self.player_repository.create_player(
            "Maija Meikäläinen", 10, self.test_team.team_id)
        self.player_repository.create_player(
            "Taija Teikäläinen", 7, self.test_team.team_id)

        players = self.player_repository.get_team_players(
            self.test_team.team_id)
        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, "Maija Meikäläinen")
        self.assertEqual(players[1].name, "Taija Teikäläinen")

    def test_get_team_players_when_none(self):
        """Test that empty list is returned when team has no players"""
        players = self.player_repository.get_team_players(
            self.test_team.team_id)
        self.assertEqual(len(players), 0)
