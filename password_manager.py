from dbm import sqlite3

from data_manager import DataManager
from utils.encryption import EncryptionManager
from utils.password_generation import generate_strong_password
from utils.logger import Logger
from utils.password_validation import validate_password_strength

class PasswordManager:
    """
    Manages passwords by encrypting them and interacting with the DataManager for storage.
    """

    def __init__(self, db_path="data/passwords.db", key_file="data/key.key", log_file="logs/app.log"):
        """
        Initializes the PasswordManager.

        Args:
            db_path (str): Path to the SQLite database file.
            key_file (str): Path to the encryption key file.
        """
        self.data_manager = DataManager(db_path=db_path)
        self.encryption_manager = EncryptionManager(key_file=key_file)
        self.logger = Logger(log_file=log_file)

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
        # Walidacja czy pola nie sa puste
        if not website or not email or not password:
            self.logger.error("Website, email, or password is missing.")
            return "All fields (website, email, password) are required."

        # Walidacja siły hasła
        is_valid, validation_messages = validate_password_strength(password)
        if not is_valid:
            self.logger.error(f"Failed to save password for {website}: {validation_messages}")
            return f"Password is too weak:\n" + "\n".join(validation_messages)

        # Zapisanie zaszyfrowanego hasła
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

    def close(self):
        """
        Closes the database connection.
        """
        try:
            self.data_manager.close()
            self.logger.info("Database connection closed.")
        except Exception as e:
            self.logger.error(f"Failed to close the database connection: {str(e)}")

