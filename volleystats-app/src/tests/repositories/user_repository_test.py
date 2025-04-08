import unittest
from repositories.user_repository import UserRepository
from initialize_database import initialize_database


class TestUserRepository(unittest.TestCase):
    def setUp(self):
        initialize_database()
        self.user_repository = UserRepository()

    def test_create_user(self):
        """Test that user can be created"""
        user = self.user_repository.create_user("Paavo", "Kissa123")
        self.assertEqual(user.username, "Paavo")
        self.assertEqual(user.password, "Kissa123")

    def test_find_by_username_existing_user(self):
        """Test that existing user can be found"""
        self.user_repository.create_user("Paavo", "Kissa123")
        user = self.user_repository.find_by_username("Paavo")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "Paavo")

    def test_find_by_username_nonexistent_user(self):
        """Test that nonexistent user returns None"""
        user = self.user_repository.find_by_username("Sirpa")
        self.assertIsNone(user)

    def test_create_duplicate_user(self):
        """Test that a used username cannot be created"""
        self.user_repository.create_user("Paavo", "Kissa123")
        result = self.user_repository.create_user("Paavo", "Koira123")
        self.assertIsNone(result)

    def test_delete_all_users(self):
        """Test that all users can be deleted from the database"""
        self.user_repository.create_user("Paavo", "Kissa123")
        delete = self.user_repository.delete_all()
        self.assertEqual(delete, None)