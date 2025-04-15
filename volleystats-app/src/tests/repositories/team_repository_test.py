import unittest
from repositories.team_repository import TeamRepository
from repositories.user_repository import UserRepository
from initialize_database import initialize_database


class TestTeamRepository(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.team_repository = TeamRepository()
        self.user_repository = UserRepository()

        # Create a test user
        self.test_user = self.user_repository.create_user("Paavo", "Kissa123")

    def test_create_team(self):
        """Test that creating a team works"""
        team = self.team_repository.create_team(
            "VolleyStars", self.test_user.id)
        self.assertEqual(team.name, "VolleyStars")
        self.assertEqual(team.user_id, self.test_user.id)

    def test_get_user_teams(self):
        """Test that getting a user's teams works"""
        self.team_repository.create_team("VolleyStars", self.test_user.id)
        self.team_repository.create_team("VolleySuns", self.test_user.id)

        teams = self.team_repository.get_user_teams(self.test_user.id)
        self.assertEqual(len(teams), 2)
        self.assertEqual(teams[0].name, "VolleyStars")
        self.assertEqual(teams[1].name, "VolleySuns")

    def test_get_user_teams_when_none(self):
        """Test that empty list is returned when user has no teams"""
        teams = self.team_repository.get_user_teams(self.test_user.id)
        self.assertEqual(len(teams), 0)
