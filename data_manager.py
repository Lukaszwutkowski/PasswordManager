import sqlite3
from contextlib import contextmanager
from utils.encryption import EncryptionManager


class DataManager:
    """
    Manages data persistence using SQLite for storing passwords.
    Provides automatic handling of database connections.
    """

    def __init__(self, db_path="data/passwords.db", key_file="data/key.key", key=None):
        """
        Initializes the DataManager and ensures that the necessary tables exist.

        Args:
            db_path (str): Path to the SQLite database file.
            key_file (str): Path to the encryption key file.
            key (bytes): Encryption key. If provided, key_file is ignored.
        """
        self.db_path = db_path
        self.key_file = key_file
        self.key = key
        self.encryption_manager = EncryptionManager(key_file=self.key_file, key=self.key)
        self.ensure_tables_exist()
        self.ensure_admin_user()

    @contextmanager
    def database_connection(self):
        """
        A context manager for handling database connections.
        Ensures that the connection is closed after use.

        Yields:
            sqlite3.Connection: An open database connection.
        """
        conn = None
        try:
            conn = sqlite3.connect(self.db_path)
            yield conn
        except sqlite3.Error as e:
            print(f"Database connection error: {str(e)}")
        finally:
            if conn:
                conn.close()

    def ensure_tables_exist(self):
        """
        Ensures that the required database tables exist.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY,
                    website TEXT NOT NULL,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            """)
            conn.commit()

    def ensure_admin_user(self):
        """
        Ensures that the default admin user exists in the database.
        Creates the admin user if it does not exist.
        """
        default_username = "admin"
        default_password = "password123"

        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users WHERE username = ?", (default_username,))
            admin_exists = cursor.fetchone()[0] > 0

            if not admin_exists:
                encrypted_password = self.encryption_manager.encrypt(default_password)
                cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                               (default_username, encrypted_password))
                conn.commit()
                print("Default admin user created with username 'admin' and password 'password123'.")
            else:
                print("Admin user already exists.")

    def get_user_by_username(self, username):
        """
        Retrieves a user's encrypted password by their username.

        Args:
            username (str): The username to search for.

        Returns:
            tuple or None: (encrypted_password,) if the user exists, otherwise None.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            return cursor.fetchone()

    def update_admin_password(self, new_password):
        """
        Updates the admin user's password in the database.

        Args:
            new_password (str): The new password to encrypt and save.
        """
        encrypted_password = self.encryption_manager.encrypt(new_password)
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET password = ? WHERE username = 'admin'", (encrypted_password,))
            conn.commit()

    def save_password(self, website, email, password):
        """
        Saves an encrypted password to the database.

        Args:
            website (str): The website name.
            email (str): The email or username.
            password (str): The encrypted password to save.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO passwords (website, email, password)
                VALUES (?, ?, ?)
            """, (website, email, password))
            conn.commit()

    def get_passwords(self):
        """
        Retrieves all passwords stored in the database.

        Returns:
            list of tuples: A list of (website, email, password) entries.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT website, email, password FROM passwords")
            return cursor.fetchall()

    def search_password(self, website):
        """
        Searches for a password in the database by website name.

        Args:
            website (str): The website to search for.

        Returns:
            tuple or None: A tuple (website, email, password) if found, otherwise None.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT website, email, password FROM passwords
                WHERE LOWER(website) = ?
            """, (website.lower(),))
            return cursor.fetchone()

    def update_password(self, website, new_encrypted_password):
        """
        Updates the password for a given website.

        Args:
            website (str): The website name.
            new_encrypted_password (str): The new encrypted password to update.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE passwords
                SET password = ?
                WHERE LOWER(website) = ?
            """, (new_encrypted_password, website.lower()))
            conn.commit()

    def delete_password(self, website):
        """
        Deletes a password for the given website from the database.

        Args:
            website (str): The website whose password needs to be deleted.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE LOWER(website) = ?", (website.lower(),))
            conn.commit()

    def clear_table(self, table_name="passwords"):
        """
        Clears all data from a specified table.

        Args:
            table_name (str): The name of the table to clear.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(f"DELETE FROM {table_name}")
            conn.commit()
