import unittest
from utils.password_generation import generate_strong_password
from utils.password_validation import validate_password_strength

class TestPasswordGeneration(unittest.TestCase):
    """
    Unit tests for password generation functionality.
    """

    def test_generate_strong_password_length(self):
        """
        Test that the generated password has the correct length.
        """
        password = generate_strong_password(length=16)
        self.assertEqual(len(password), 16)

    def test_generate_strong_password_strength(self):
        """
        Test that the generated password is strong and passes validation.
        """
        password = generate_strong_password(length=12)
        is_valid, messages = validate_password_strength(password)
        self.assertTrue(is_valid)
        self.assertEqual(len(messages), 0)

    def test_generate_short_password(self):
        """
        Test that generating a password with length less than 8 raises an error.
        """
        with self.assertRaises(ValueError):
            generate_strong_password(length=6)

if __name__ == "__main__":
    unittest.main()
