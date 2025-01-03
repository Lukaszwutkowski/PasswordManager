
import configparser
import os

import bcrypt
from data_manager import DataManager
from utils.encryption import EncryptionManager
from utils.password_generation import generate_strong_password
from utils.logger import Logger
from utils.password_validation import PasswordValidator

class PasswordManager:
    """
    Manages passwords by encrypting them and interacting with the DataManager for storage.
    """

    CONFIG_FILE = "data/config.ini"

    def __init__(self, db_path="data/passwords.db", key_file="data/key.key",
                 log_file="logs/app.log", key=None):
        """
        Initializes the PasswordManager, checks for first-time setup, and ensures admin user exists.

        Args:
            db_path (str): Path to the SQLite database file.
            key_file (str): Path to the encryption key file.
            log_file (str): Path to the log file.
            key (bytes): Encryption key. If provided, key_file is ignored.
        """
        self.encryption_manager = EncryptionManager(key_file=key_file, key=key)
        self.data_manager = DataManager(db_path=db_path)
        self.logger = Logger(log_file=log_file)
        self.key_file = key_file
        self.key = key

        # Ensure necessary directories and admin user
        self._ensure_directories()
        self.data_manager.ensure_admin_user()

    def _ensure_directories(self):
        """
        Ensures that required directories exist.
        """
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)

    def is_configured(self):
        """
        Checks if the application has already been configured by looking for the config file.

        Returns:
            bool: True if the app is configured, False otherwise.
        """
        if not os.path.exists(self.CONFIG_FILE):
            return False
        config = configparser.ConfigParser()
        config.read(self.CONFIG_FILE)
        return config.getboolean("SETTINGS", "Configured", fallback=False)

    def set_master_password(self):
        """
        Prompts the user to set and confirm a master password.
        Ensures the password meets security requirements.
        """
        while True:
            master_password = input("Set your master password: ")
            is_valid, messages = PasswordValidator.validate_password_strength(master_password)
            if not is_valid:
                print("Password is too weak:\n" + "\n".join(messages))
                continue

            confirm_password = input("Confirm your master password: ")
            if master_password != confirm_password:
                print("Passwords do not match. Please try again.")
                continue

            self.save_master_password(master_password)
            print("Master password set successfully.")
            break

    def save_master_password(self, password):
        """
        Hashes and saves the master password in the database.

        Args:
            password (str): The master password to be hashed and stored.
        """
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        self.data_manager.update_admin_password(hashed_password)

    def mark_as_configured(self):
        """
        Marks the application as configured by creating/updating the config file.
        """
        os.makedirs(os.path.dirname(self.CONFIG_FILE), exist_ok=True)
        config = configparser.ConfigParser()
        config["SETTINGS"] = {"Configured": "True"}
        with open(self.CONFIG_FILE, "w") as config_file:
            config.write(config_file)

    def validate_user_credentials(self, username, password):
        """
        Validates user login credentials.

        Args:
            username (str): The entered username.
            password (str): The entered password.

        Returns:
            bool: True if credentials are valid, False otherwise.
        """
        user_record = self.data_manager.get_user_by_username(username)
        if user_record:
            hashed_password = user_record[0]
            # Ensure hashed_password is bytes
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode()
            elif isinstance(hashed_password, memoryview):
                hashed_password = hashed_password.tobytes()
            # Verify the password using bcrypt
            return bcrypt.checkpw(password.encode(), hashed_password)
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

        # Hash the new password with salt
        hashed_password = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt())

        # Update the password in the database
        self.data_manager.update_admin_password(hashed_password)
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
        except Exception as e:
            self.logger.error(f"Error retrieving password: {str(e)}")
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
        if not existing_record:
            self.logger.warning(f"Failed to update password: {website} not found.")
            return "Error: Website not found."

        encrypted_password = self.encryption_manager.encrypt(new_password)
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
        # Fetch the hashed password for the admin user
        user_record = self.data_manager.get_user_by_username("admin")
        if user_record:
            hashed_password = user_record[0]
            # Ensure hashed_password is bytes
            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode()
            elif isinstance(hashed_password, memoryview):
                hashed_password = hashed_password.tobytes()
            # Verify the password using bcrypt
            return bcrypt.checkpw(current_password.encode(), hashed_password)
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
