import re

class PasswordValidator:
    """
       Utility class for password-related operations such as validation and management.
    """

    @staticmethod
    def validate_password_strength(password):
        """
        Validates the strength of a password.

        Args:
            password (str): The password to validate.

        Returns:
            tuple: (bool, list) A tuple containing a boolean indicating if the password is strong
                   and a list of validation messages.
        """
        messages = []
        is_valid = True

        # Minimum length check
        if len(password) < 8:
            is_valid = False
            messages.append("Password must be at least 8 characters long.")

        # Uppercase and lowercase letter check
        if not any(char.islower() for char in password) or not any(char.isupper() for char in password):
            is_valid = False
            messages.append("Password must contain both uppercase and lowercase letters.")

        # Digit check
        if not any(char.isdigit() for char in password):
            is_valid = False
            messages.append("Password must contain at least one digit.")

        # Special character check
        if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            is_valid = False
            messages.append("Password must contain at least one special character (!@#$%^&*(), etc.).")

        return is_valid, messages
