import os
from cryptography.fernet import Fernet

class PasswordManager:
    """
        Manages saving, retrieving, and searching for passwords.

        Attributes:
            file_path (str): Path to the file where passwords are stored.
            key_file (str): Path to the file storing the encryption key.
        """
    def __init__(self, file_path, key_file="data/key.key"):
        """
                Initializes the PasswordManager and loads or generates the encryption key.

                Args:
                    file_path (str): Path to the file where passwords are stored.
                    key_file (str): Path to the encryption key file. Defaults to "data/key.key".
        """
        self.file_path = file_path
        self.key_file = key_file
        self.cipher_suite = self.load_or_generate_key()

    def load_or_generate_key(self):
        """
        Loads the encryption key from the file or generates a new one.

        Returns:
            Fernet: Cipher object for encryption and decryption.
        """
        if not os.path.exists(self.key_file):
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
        else:
            with open(self.key_file, "rb") as key_file:
                key = key_file.read()
        return Fernet(key)

    def save_password(self, website, email, password):
        """
                Saves an encrypted password to the file.

                Args:
                    website (str): The website name.
                    email (str): The email or username.
                    password (str): The password to save.
        """
        encrypted_password = self.cipher_suite.encrypt(password.encode())
        with open(self.file_path, "a") as file:
            file.write(f"{website}:{email}:{encrypted_password.decode()}\n")

    def search_password(self, website):
        """
        Searches for a password by website name.

        Args:
            website (str): The name of the website.

        Returns:
            str: The details of the website, email, and password, or "Not found".
        """
        passwords = self.read_passwords()
        for site, email, password in passwords:
            if site.lower() == website.lower():
                return f"Website: {site}, Email: {email}, Password: {password}"
        return "Not found"

    def read_passwords(self):
        """
        Reads all passwords from the file and decrypts them.

        Returns:
            list: A list of tuples containing website, email, and decrypted password.
        """
        if not os.path.exists(self.file_path):
            return []

        passwords = []
        with open(self.file_path, "r") as file:
            for line in file:
                try:
                    website, email, encrypted_password = line.strip().split(":")
                    decrypted_password = self.cipher_suite.decrypt(encrypted_password.encode()).decode()
                    passwords.append((website, email, decrypted_password))
                except ValueError:
                    # Skip malformed lines
                    pass
        return passwords
