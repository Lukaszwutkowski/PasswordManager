
import os
import unittest
from password_manager import PasswordManager

class TestPasswordManager(unittest.TestCase):
    """
    Unit tests for the PasswordManager class.
    """

    def setUp(self):
        """
        Sets up a temporary test environment before each test.
        Creates test database and encryption key file.
        """
        self.test_db_path = "test_data/passwords_test.db"
        self.test_key_file = "test_data/key_test.key"

        os.makedirs("test_data", exist_ok=True)

        # Remove existing test files
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)

        # Initialize the PasswordManager with test paths
        self.manager = PasswordManager(db_path=self.test_db_path, key_file=self.test_key_file)

    def tearDown(self):
        """
        Cleans up the test environment after each test.
        Deletes the test database and encryption key file.
        """
        # Clear all database entries
        self.manager.data_manager.clear_table()

        # Close any open connections
        self.manager.data_manager.close()

        # Remove the test database file
        if os.path.exists(self.test_db_path):
            os.remove(self.test_db_path)

        # Remove the encryption key file
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)

        # Remove the test_data directory if empty
        if os.path.exists("test_data") and not os.listdir("test_data"):
            os.rmdir("test_data")

    def test_save_password(self):
        """
        Tests saving a password to the database.
        """
        result = self.manager.save_password("example.com", "user@example.com", "Password123!")
        self.assertIn("successfully", result.lower())

        passwords = self.manager.get_passwords()
        self.assertEqual(len(passwords), 1)
        self.assertEqual(passwords[0], ("example.com", "user@example.com", "Password123!"))

    def test_validate_user_credentials(self):
        """
        Test validating admin credentials after updating the password.
        """
        # Update the admin password
        result = self.manager.update_admin_password("AdminNewPassword1!")
        self.assertIn("successfully", result.lower())

        # Validate the updated admin credentials
        is_valid = self.manager.validate_user_credentials("admin", "AdminNewPassword1!")
        self.assertTrue(is_valid)

        # Test invalid credentials
        is_invalid = self.manager.validate_user_credentials("admin", "WrongPassword!")
        self.assertFalse(is_invalid)

    def test_update_admin_password(self):
        """
        Tests updating the admin password and validates it.
        """
        # Update the admin password
        update_result = self.manager.update_admin_password("NewSecurePassword!1")
        self.assertIn("successfully", update_result.lower())

        # Validate the updated password
        is_valid = self.manager.validate_user_credentials("admin", "NewSecurePassword!1")
        self.assertTrue(is_valid)

        # Test invalid credentials
        is_invalid = self.manager.validate_user_credentials("admin", "WrongPassword!")
        self.assertFalse(is_invalid)

    def test_save_weak_password(self):
        """
        Test that saving a weak password returns an appropriate validation error.
        """
        weak_password = "password123"
        result = self.manager.save_password("example.com", "user@example.com", weak_password)
        self.assertIn("Password is too weak", result)

    def test_search_password(self):
        """
        Test that searching for a password works correctly.
        """
        self.manager.save_password("example.com", "user@example.com", "pasSswo?rd123")
        result = self.manager.search_password("example.com")
        self.assertEqual(result, "Website: example.com, Email: user@example.com, Password: pasSswo?rd123")

    def test_search_password_not_found(self):
        """
        Test that searching for a non-existent website returns 'Not found'.
        """
        result = self.manager.search_password("nonexistent.com")
        self.assertEqual(result, "Not found")

    def test_save_and_load_multiple_passwords(self):
        """
        Test saving and loading multiple passwords.
        """
        passwords_to_save = [
            ("example.com", "user1@example.com", "pasSswo?rd123"),
            ("test.com", "user2@test.com", "pasSswo?rd123"),
            ("sample.org", "user3@sample.org", "pasSswo?rd123"),
        ]

        for website, email, password in passwords_to_save:
            self.manager.save_password(website, email, password)

        passwords = self.manager.get_passwords()
        self.assertEqual(len(passwords), 3)
        self.assertIn(("example.com", "user1@example.com", "pasSswo?rd123"), passwords)

    def test_update_password(self):
        """
        Test updating the password for an existing website.
        """
        # Save an initial password
        save_result = self.manager.save_password("example.com", "user@example.com", "OldPassword!1")
        self.assertIn("successfully", save_result.lower())

        # Update the password
        update_result = self.manager.update_password("example.com", "NewStrongPassword!1")
        self.assertIn("successfully", update_result.lower())

        # Verify the password was updated
        updated_record = self.manager.search_password("example.com")
        self.assertIn("NewStrongPassword!1", updated_record)

    def test_delete_password(self):
        """
        Test deleting a password from the database.
        """
        # Save a password
        self.manager.save_password("example.com", "user@example.com", "Password123!")

        # Delete the password
        delete_result = self.manager.delete_password("example.com")
        self.assertIn("successfully", delete_result.lower())

        # Verify the password was deleted
        result = self.manager.search_password("example.com")
        self.assertEqual(result, "Not found")

if __name__ == "__main__":
    unittest.main()
