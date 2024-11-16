from data_manager import DataManager
from utils.encryption import EncryptionManager

class PasswordManager:
    """
    Manages passwords by encrypting them and interacting with the DataManager for storage.
    """

    def __init__(self, db_path="data/passwords.db", key_file="data/key.key"):
        """
        Initializes the PasswordManager.

        Args:
            db_path (str): Path to the SQLite database file.
            key_file (str): Path to the encryption key file.
        """
        self.data_manager = DataManager(db_path=db_path)
        self.encryption_manager = EncryptionManager(key_file=key_file)

    def save_password(self, website, email, password):
        """
        Encrypts and saves a password to the database.

        Args:
            website (str): The website name.
            email (str): The email or username.
            password (str): The plaintext password to save.
        """
        encrypted_password = self.encryption_manager.encrypt(password)
        self.data_manager.save_password(website, email, encrypted_password)

    def get_passwords(self):
        """
        Retrieves all decrypted passwords from the database.

        Returns:
            list of tuples: List of (website, email, decrypted password).
        """
        passwords = self.data_manager.get_passwords()
        return [
            (website, email, self.encryption_manager.decrypt(password))
            for website, email, password in passwords
        ]

    def search_password(self, website):
        """
        Searches for a password by website.

        Args:
            website (str): The website name.

        Returns:
            str: Details of the website, email, and password, or "Not found".
        """
        result = self.data_manager.search_password(website)
        if result:
            website, email, encrypted_password = result
            password = self.encryption_manager.decrypt(encrypted_password)
            return f"Website: {website}, Email: {email}, Password: {password}"
        return "Not found"

    def close(self):
        """
        Closes the database connection.
        """
        self.data_manager.close()
