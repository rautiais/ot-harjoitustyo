import unittest
from services.user_service import UserService

class TestUserService(unittest.TestCase):
    def setUp(self):
        self.user_service = UserService()

    def test_create_user_valid_credentials(self):
        result = self.user_service.create_user("Paavo", "Kissa123")
        self.assertTrue(result)