import unittest
from services.user_service import UserService
from initialize_database import initialize_database


class TestUserService(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.user_service = UserService()

    def test_create_user_with_valid_credentials(self):
        """Test that creating user with valid credentials works"""
        result = self.user_service.create_user("Paavo", "Kissa123")
        self.assertTrue(result)

    def test_create_user_with_too_short_username(self):
        """Test that creating user with too short username doesn't work"""
        result = self.user_service.create_user("Pa", "Kissa123")
        self.assertFalse(result)

    def test_create_user_with_too_short_password(self):
        """Test that creating user with too short password doesn't work"""
        result = self.user_service.create_user("Paavo", "Kissa")
        self.assertFalse(result)

    def test_create_duplicate_user(self):
        """Test that a used username cannot be created"""
        self.user_service.create_user("Paavo", "Kissa123")
        result = self.user_service.create_user("Paavo", "Koira123")
        self.assertFalse(result)

    def test_login_with_valid_credentials(self):
        """Test that logging in with valid credentials works"""
        self.user_service.create_user("Paavo", "Kissa123")
        result = self.user_service.login("Paavo", "Kissa123")
        self.assertTrue(result)

    def test_login_with_invalid_username(self):
        """Test that logging in with invalid username doesn't work"""
        self.user_service.create_user("Paavo", "Kissa123")
        result = self.user_service.login("Sirpa", "Kissa123")
        self.assertFalse(result)

    def test_login_with_invalid_password(self):
        """Test that logging in with invalid password doesn't work"""
        self.user_service.create_user("Paavo", "Kissa123")
        result = self.user_service.login("Paavo", "Koira123")
        self.assertFalse(result)

    def test_logging_out(self):
        """Test that logging out works"""
        self.user_service.logout()
        self.assertIsNone(self.user_service.get_current_user())
