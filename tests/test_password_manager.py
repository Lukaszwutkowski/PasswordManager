import  os
import unittest
from unittest import TestCase
from password_manager import PasswordManager


class TestPasswordManager(TestCase):
    """
       Unit tests for the PasswordManager class.
    """

    def setUp(self):
        """
            Set up a test environment before each test.
        """
        self.test_file = "test_data.txt"
        self.test_key_file = "test_key.key"
        self.manager = PasswordManager(file_path=self.test_file, key_file=self.test_key_file)

    def tearDown(self):
        """
            Clean up after each test by removing test files.
        """
        if os.path.exists(self.test_file):
            os.remove(self.test_file)
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)

    def test_load_or_generate_key(self):
        """
        Test that the encryption key is generated when the key file does not exist,
        and that the same key is loaded when the file exists.
        """
        # Ensure the key file does not exist
        if os.path.exists(self.test_key_file):
            os.remove(self.test_key_file)
        self.assertFalse(os.path.exists(self.test_key_file))

        # Generate a new key and verify the file is created
        manager = PasswordManager(file_path=self.test_file, key_file=self.test_key_file)
        cipher1 = manager.load_or_generate_key()
        self.assertTrue(os.path.exists(self.test_key_file))

        # Reload the key and verify it is the same
        cipher2 = manager.load_or_generate_key()
        self.assertEqual(cipher1._signing_key, cipher2._signing_key)

    def test_save_password(self):
        """
            Test that saving a password works as expected.
        """
        self.manager.save_password("example.com", "user@example.com", "password")
        with open(self.test_file, "r") as file:
            data = file.read()
        self.assertIn("example.com", data)
        self.assertIn("user@example.com", data)

    def test_search_password(self):
        """
            Test that searching for a password works correctly.
        """
        self.manager.save_password("example.com", "user@example.com", "password")
        result = self.manager.search_password("example.com")
        self.assertEqual(result, "Website: example.com, Email: user@example.com, Password: password")

    def test_search_password_not_found(self):
        """
        Test that searching for a non-existent website returns 'Not found'.
        """
        result = self.manager.search_password("none_exist.com")
        self.assertEqual(result, "Not found")

    def test_search_password_case_insensitive(self):
        """
        Test that searching for a password is case-insensitive.
        """
        self.manager.save_password("Example.com", "user@example.com", "password123")
        result = self.manager.search_password("example.com")
        self.assertEqual(result, "Website: Example.com, Email: user@example.com, Password: password123")

    def test_read_passwords(self):
        """
            Test that reading passwords returns decrypted data correctly.
        """
        self.manager.save_password("example.com", "user@example.com", "password")
        passwords = self.manager.read_passwords()
        self.assertEqual(len(passwords), 1)
        self.assertEqual(passwords[0], ("example.com", "user@example.com", "password"))

    def test_read_passwords_empty_file(self):
        """
            Test that reading from an empty file returns an empty list.
        """
        passwords = self.manager.read_passwords()
        self.assertEqual(passwords, [])

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

        passwords = self.manager.read_passwords()
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
        passwords = self.manager.read_passwords()
        self.assertEqual(passwords[0], ("example.com", "user@example.com", special_password))

    def test_read_passwords_with_corrupted_file(self):
        """
        Test that the program handles corrupted file data gracefully.
        Only valid lines should be processed.
        """
        # Write corrupted data and a valid entry to the test file
        with open(self.test_file, "w") as file:
            file.write("corrupted data\n")
            file.write("example.com:user@example.com:{}\n".format(
                self.manager.cipher_suite.encrypt("password123".encode()).decode()
            ))

        # Read passwords and verify only the valid entry is returned
        passwords = self.manager.read_passwords()
        self.assertEqual(len(passwords), 1)
        self.assertEqual(passwords[0], ("example.com", "user@example.com", "password123"))

if __name__ == "__main__":
    unittest.main()
