from cryptography.fernet import Fernet
import os

class EncryptionManager:
    """
    Handles encryption and decryption of data using Fernet.
    """

    def __init__(self, key_file="data/key.key"):
        """
        Initializes the EncryptionManager and loads or generates the encryption key.

        Args:
            key_file (str): Path to the encryption key file.
        """
        self.key_file = key_file
        self.cipher_suite = self._load_or_generate_key()

    def _load_or_generate_key(self):
        """
        Loads the encryption key from the file or generates a new one.

        Returns:
            Fernet: Cipher object for encryption and decryption.
        """
        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, "rb") as key_file:
                    key = key_file.read()
                    # Validate the key
                    return Fernet(key)
            except (ValueError, Exception) as e:
                print(f"Invalid key detected. Generating a new one. Error: {e}")
                # If invalid key detected - Generate a new one
                key = Fernet.generate_key()
                with open(self.key_file, "wb") as key_file:
                    key_file.write(key)
                return Fernet(key)
        else:
            # File does not exist - Generate a new one
            key = Fernet.generate_key()
            with open(self.key_file, "wb") as key_file:
                key_file.write(key)
            return Fernet(key)

    def encrypt(self, plaintext):
        """
        Encrypts the given plaintext.

        Args:
            plaintext (str): The plaintext to encrypt.

        Returns:
            str: The encrypted text.
        """
        return self.cipher_suite.encrypt(plaintext.encode()).decode()

    def decrypt(self, encrypted_text):
        """
        Decrypts the given encrypted text.

        Args:
            encrypted_text (str): The encrypted text to decrypt.

        Returns:
            str: The decrypted plaintext.
        """
        return self.cipher_suite.decrypt(encrypted_text.encode()).decode()
