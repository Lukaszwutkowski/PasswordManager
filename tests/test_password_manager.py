import os
import unittest
from password_manager import PasswordManager

class TestPasswordManager(unittest.TestCase):
    """
    Unit tests for the PasswordManager class.
    """

    def setUp(self):
        """
        Set up a test environment before each test.
        Creates test database and key file.
        """
        self.test_db_path = "test_passwords.db"
        self.test_key_file = "test_key.key"
        self.manager = PasswordManager(db_path=self.test_db_path, key_file=self.test_key_file)

    def tearDown(self):
        """
        Clean up after each test by removing test database and key file.
        """
        # Clear the database table
        self.manager.data_manager.clear_table()

        # Close database connection
        self.manager.close()

        # Remove database file
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        # Remove key file
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)

    def test_save_password(self):
        """
        Test that saving a password works as expected.
        """
        self.manager.save_password("example.com", "user@example.com", "password123")
        passwords = self.manager.get_passwords()
        self.assertEqual(len(passwords), 1)
        self.assertEqual(passwords[0], ("example.com", "user@example.com", "password123"))

    def test_search_password(self):
        """
        Test that searching for a password works correctly.
        """
        self.manager.save_password("example.com", "user@example.com", "password123")
        result = self.manager.search_password("example.com")
        self.assertEqual(result, "Website: example.com, Email: user@example.com, Password: password123")

    def test_search_password_not_found(self):
        """
        Test that searching for a non-existent website returns 'Not found'.
        """
        result = self.manager.search_password("nonexistent.com")
        self.assertEqual(result, "Not found")

    def test_search_password_case_insensitive(self):
        """
        Test that searching for a password is case-insensitive.
        """
        self.manager.save_password("Example.com", "user@example.com", "password123")
        result = self.manager.search_password("example.com")
        self.assertEqual(result, "Website: Example.com, Email: user@example.com, Password: password123")

    def test_save_and_load_multiple_passwords(self):
        """
        Test saving and loading multiple passwords.
        """
        passwords_to_save = [
            ("example.com", "user1@example.com", "password1"),
            ("test.com", "user2@test.com", "password2"),
            ("sample.org", "user3@sample.org", "password3"),
        ]

        for website, email, password in passwords_to_save:
            self.manager.save_password(website, email, password)

        passwords = self.manager.get_passwords()
        self.assertEqual(len(passwords), 3)
        self.assertIn(("example.com", "user1@example.com", "password1"), passwords)
        self.assertIn(("test.com", "user2@test.com", "password2"), passwords)
        self.assertIn(("sample.org", "user3@sample.org", "password3"), passwords)

    def test_save_password_with_special_characters(self):
        """
        Test saving a password with special characters.
        """
        special_password = "!@#$%^&*()_+{}|:\"<>?"
        self.manager.save_password("example.com", "user@example.com", special_password)
        passwords = self.manager.get_passwords()
        self.assertEqual(passwords[0], ("example.com", "user@example.com", special_password))

    def test_empty_database(self):
        """
        Test that an empty database returns an empty list.
        """
        passwords = self.manager.get_passwords()
        self.assertEqual(passwords, [])

if __name__ == "__main__":
    unittest.main()
