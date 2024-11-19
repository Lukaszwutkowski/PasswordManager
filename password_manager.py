from dbm import sqlite3

from data_manager import DataManager
from utils.encryption import EncryptionManager
from utils.password_generation import generate_strong_password
from utils.logger import Logger
from utils.password_validation import PasswordValidator

class PasswordManager:
    """
    Manages passwords by encrypting them and interacting with the DataManager for storage.
    """

    def __init__(self, db_path="data/passwords.db", key_file="data/key.key", log_file="logs/app.log", key=None):
        """
        Initializes the PasswordManager.

        Args:
            db_path (str): Path to the SQLite database file.
            key_file (str): Path to the encryption key file.
            key (bytes): Encryption key. If provided, key_file is ignored.
        """
        self.encryption_manager = EncryptionManager(key_file=key_file, key=key)
        self.data_manager = DataManager(db_path=db_path, key_file=key_file, key=key)
        self.logger = Logger(log_file=log_file)
        self.key_file = key_file
        self.key = key

    def validate_user_credentials(self, username, password):
        """
        Validates user login credentials.

        Args:
            username (str): The entered username.
            password (str): The entered password.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        # Fetch the encrypted password for the given username
        user_record = self.data_manager.get_user_by_username(username)
        if user_record:
            encrypted_password = user_record[0]
            decrypted_password = self.encryption_manager.decrypt(encrypted_password)
            return decrypted_password == password
        return False

    def update_admin_password(self, new_password):
        """
        Updates the admin password in the database.

        Args:
            new_password (str): The new password to set.

        Returns:
            str: Success or validation error message.
        """
        # Validate password strength
        is_valid, messages = PasswordValidator.validate_password_strength(new_password)
        if not is_valid:
            return f"Password is too weak:\n" + "\n".join(messages)

        # Update the password in the database
        self.data_manager.update_admin_password(new_password)
        return "Admin password updated successfully!"

    def save_password(self, website, email, password):
        """
        Encrypts and saves a password to the database after validating it.

        Args:
            website (str): The website name.
            email (str): The email or username.
            password (str): The plaintext password to save.

        Returns:
            str: Success message or validation errors.
        """
        if not website or not email or not password:
            self.logger.error("Website, email, or password is missing.")
            return "All fields (website, email, password) are required."

        is_valid, validation_messages = PasswordValidator.validate_password_strength(password)
        if not is_valid:
            self.logger.error(f"Failed to save password for {website}: {validation_messages}")
            return f"Password is too weak:\n" + "\n".join(validation_messages)

        encrypted_password = self.encryption_manager.encrypt(password)
        self.data_manager.save_password(website, email, encrypted_password)
        self.logger.info(f"Password for {website} saved successfully.")
        return "Password saved successfully."

    def get_passwords(self):
        """
        Retrieves all decrypted passwords from the database.

        Returns:
            list of tuples: List of (website, email, decrypted password).
        """
        try:
            passwords = self.data_manager.get_passwords()
            decrypted_passwords = [
                (website, email, self.encryption_manager.decrypt(password))
                for website, email, password in passwords
            ]
            self.logger.info("Retrieved all passwords from the database.")
            return decrypted_passwords
        except Exception as e:
            self.logger.error(f"Failed to retrieve passwords: {str(e)}")
            return []

    def search_password(self, website):
        """
        Searches for a password by website.

        Args:
            website (str): The website name.

        Returns:
            str: Details of the website, email, and password, or "Not found".
        """
        try:
            result = self.data_manager.search_password(website)
            if result:
                website, email, encrypted_password = result
                password = self.encryption_manager.decrypt(encrypted_password)
                self.logger.info(f"Password for {website} retrieved successfully.")
                return f"Website: {website}, Email: {email}, Password: {password}"
            self.logger.warning(f"Password for {website} not found.")
            return "Not found"
        except sqlite3.Error as e:
            self.logger.error(f"Database error: {str(e)}")
            return "Database error occurred while searching for the password."
        except Exception as e:
            self.logger.error(f"Error decrypting password: {str(e)}")
            return "Error occurred while searching for the password."

    def generate_strong_password(self, length=12):
        """
        Generates a strong password.

        Args:
            length (int): The desired length of the password. Default is 12.

        Returns:
            str: A strong, randomly generated password.
        """
        return generate_strong_password(length)

    def update_password(self, website, new_password):
        """
        Updates the password for a given website.

        Args:
            website (str): The website name.
            new_password (str): The new plaintext password.

        Returns:
            str: A success message or an error if the website was not found or the password is invalid.
        """
        self.logger.info(f"Attempting to update password for website: {website}")

        is_valid, validation_messages = PasswordValidator.validate_password_strength(new_password)
        if not is_valid:
            self.logger.error(f"Failed to update password for {website}: {validation_messages}")
            return f"Password is too weak:\n" + "\n".join(validation_messages)

        existing_record = self.data_manager.search_password(website)
        self.logger.debug(f"Existing record for {website}: {existing_record}")
        if not existing_record:
            self.logger.warning(f"Failed to update password: {website} not found.")
            return "Error: Website not found."

        encrypted_password = self.encryption_manager.encrypt(new_password)
        self.logger.debug(f"Encrypted password for {website}: {encrypted_password}")
        self.data_manager.update_password(website, encrypted_password)
        self.logger.info(f"Password for {website} updated successfully.")
        return "Password updated successfully."

    def delete_password(self, website):
        """
        Deletes the password for the given website.

        Args:
            website (str): The website whose password needs to be deleted.

        Returns:
            str: A success message or an error if the website was not found.
        """
        self.logger.info(f"Attempting to delete password for website: {website}")

        # Check if the website exists in the database
        existing_record = self.data_manager.search_password(website)
        self.logger.debug(f"Existing record for {website}: {existing_record}")
        if not existing_record:
            self.logger.warning(f"Failed to delete password: {website} not found.")
            return "Error: Website not found."

        # Delete the password
        self.data_manager.delete_password(website)
        self.logger.info(f"Password for {website} deleted successfully.")
        return "Password deleted successfully."

    def validate_current_password(self, current_password):
        """
        Validates the provided current password against the stored admin password.

        Args:
            current_password (str): The current password entered by the user.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        # Fetch the encrypted password for the admin user
        user_record = self.data_manager.get_user_by_username("admin")
        if user_record:
            encrypted_password = user_record[0]
            # Decrypt the stored password
            decrypted_password = self.encryption_manager.decrypt(encrypted_password)
            # Compare the decrypted password with the provided current password
            return decrypted_password == current_password
        return False

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self.data_manager.close()
            self.logger.info("Database connection closed.")
        except Exception as e:
            self.logger.error(f"Failed to close the database connection: {str(e)}")
