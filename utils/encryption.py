
from cryptography.fernet import Fernet
import os

class EncryptionManager:
    """
    Handles encryption and decryption of data using Fernet.
    """

    def __init__(self, key_file="data/key.key", key=None):
        """
        Initializes the EncryptionManager and loads or generates the encryption key.

        Args:
            key_file (str): Path to the encryption key file.
            key (bytes): Encryption key. If provided, key_file is ignored.
        """
        if key is not None:
            self.key = key
            self.cipher_suite = Fernet(self.key)
        else:
            self.key_file = key_file
            self.cipher_suite = self._load_or_generate_key()

    def _load_or_generate_key(self):
        """
        Loads the encryption key from the file or generates a new one.

        Returns:
            Fernet: Cipher object for encryption and decryption.
        """
        os.makedirs(os.path.dirname(self.key_file), exist_ok=True)

        if os.path.exists(self.key_file):
            try:
                with open(self.key_file, "rb") as key_file:
                    key = key_file.read()
                    return Fernet(key)
            except Exception as e:
                print(f"Invalid key detected. Regenerating key. Error: {e}")

        # Generate a new key if the file does not exist or the key is invalid
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
