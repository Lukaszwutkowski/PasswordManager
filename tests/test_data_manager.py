import os
import unittest
from data_manager import DataManager

class TestDataManager(unittest.TestCase):
    """
    Unit tests for the DataManager class.
    """

    def setUp(self):
        """
        Set up a test environment before each test.
        Creates a temporary test database.
        """
        self.test_db_path = "test_passwords.db"
        self.data_manager = DataManager(db_path=self.test_db_path)

    def tearDown(self):
        """
        Clean up the test environment after each test.
        Deletes all entries in the database and closes the connection.
        """
        # Clear the database table
        self.data_manager.clear_table()

        # Close database connection
        self.data_manager.close()

        # Remove database file
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

    def test_create_table(self):
        """
        Test that the passwords table is created during initialization.
        """
        # Verify table exists by saving and retrieving a password
        self.data_manager.save_password("example.com", "user@example.com", "password123")
        passwords = self.data_manager.get_passwords()
        self.assertEqual(len(passwords), 1)

    def test_save_password(self):
        """
        Test saving a password to the database.
        """
        self.data_manager.save_password("example.com", "user@example.com", "password123")
        passwords = self.data_manager.get_passwords()
        self.assertEqual(len(passwords), 1)
        self.assertEqual(passwords[0], ("example.com", "user@example.com", "password123"))

    def test_get_passwords_empty_database(self):
        """
        Test retrieving passwords from an empty database.
        """
        passwords = self.data_manager.get_passwords()
        self.assertEqual(passwords, [])

    def test_get_passwords(self):
        """
        Test retrieving multiple passwords from the database.
        """
        passwords_to_save = [
            ("example.com", "user1@example.com", "password1"),
            ("test.com", "user2@test.com", "password2"),
            ("sample.org", "user3@sample.org", "password3"),
        ]

        for website, email, password in passwords_to_save:
            self.data_manager.save_password(website, email, password)

        passwords = self.data_manager.get_passwords()
        self.assertEqual(len(passwords), 3)
        self.assertIn(("example.com", "user1@example.com", "password1"), passwords)

    def test_search_password(self):
        """
        Test searching for a specific password by website.
        """
        self.data_manager.save_password("example.com", "user@example.com", "password123")
        result = self.data_manager.search_password("example.com")
        self.assertEqual(result, ("example.com", "user@example.com", "password123"))

    def test_search_password_not_found(self):
        """
        Test searching for a password that does not exist.
        """
        result = self.data_manager.search_password("nonexistent.com")
        self.assertIsNone(result)

if __name__ == "__main__":
    unittest.main()