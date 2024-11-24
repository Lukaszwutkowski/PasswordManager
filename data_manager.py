
import sqlite3
import os
import bcrypt
import base64
from contextlib import contextmanager

class DataManager:
    """
    Manages database interactions for storing and retrieving passwords and user data.
    """

    def __init__(self, db_path="data/passwords.db"):
        self.db_path = db_path
        self._initialize_database()

    def _initialize_database(self):
        """
        Initializes the database by creating necessary tables.
        """
        db_dir = os.path.dirname(self.db_path)
        if db_dir:
            os.makedirs(db_dir, exist_ok=True)
        with self.database_connection() as conn:
            cursor = conn.cursor()
            # Users table with password stored as TEXT
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL
                );
            """)
            # Passwords table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS passwords (
                    website TEXT PRIMARY KEY,
                    email TEXT NOT NULL,
                    password TEXT NOT NULL
                );
            """)
            conn.commit()
        # Ensure admin user exists
        self.ensure_admin_user()

    @contextmanager
    def database_connection(self):
        """
        Provides a context manager for database connections.
        Ensures that connections are properly closed after use.
        """
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def ensure_admin_user(self):
        """
        Ensures that the admin user exists in the database.
        If not, creates the admin user with a default password.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username = 'admin'")
            if not cursor.fetchone():
                default_password = 'admin123'  # Replace with a secure default
                # Hash the default password
                hashed_password = bcrypt.hashpw(default_password.encode(), bcrypt.gensalt())
                # Encode the hashed password to Base64 string
                hashed_password_b64 = base64.b64encode(hashed_password).decode('utf-8')
                cursor.execute("""
                    INSERT INTO users (username, password) VALUES (?, ?)
                """, ('admin', hashed_password_b64))
                conn.commit()

    def get_user_by_username(self, username):
        """
        Retrieves the hashed password for the given username.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result:
                hashed_password_b64 = result[0]
                # Ensure hashed_password_b64 is a string
                if isinstance(hashed_password_b64, bytes):
                    hashed_password_b64 = hashed_password_b64.decode('utf-8')
                # Decode the Base64 string back to bytes
                hashed_password = base64.b64decode(hashed_password_b64)
                return (hashed_password,)
            else:
                return None

    def update_admin_password(self, hashed_password):
        """
        Updates the admin password in the database.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            # Encode the hashed password to Base64 string
            hashed_password_b64 = base64.b64encode(hashed_password).decode('utf-8')
            cursor.execute("""
                UPDATE users SET password = ? WHERE username = 'admin'
            """, (hashed_password_b64,))
            conn.commit()

    def save_password(self, website, email, encrypted_password):
        """
        Saves an encrypted password to the database.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO passwords (website, email, password)
                VALUES (?, ?, ?)
            """, (website, email, encrypted_password))
            conn.commit()

    def get_passwords(self):
        """
        Retrieves all passwords from the database.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT website, email, password FROM passwords")
            return cursor.fetchall()

    def search_password(self, website):
        """
        Searches for a password by website.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT website, email, password FROM passwords WHERE website = ?
            """, (website,))
            return cursor.fetchone()

    def update_password(self, website, encrypted_password):
        """
        Updates the password for a given website.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE passwords SET password = ? WHERE website = ?
            """, (encrypted_password, website))
            conn.commit()

    def delete_password(self, website):
        """
        Deletes the password for the given website.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords WHERE website = ?", (website,))
            conn.commit()

    def clear_table(self):
        """
        Clears all data from the users and passwords tables.
        """
        with self.database_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords;")
            cursor.execute("DELETE FROM users;")
            conn.commit()

    def close(self):
        """
        Closes the database connection.
        (Not strictly necessary with context managers)
        """
        pass  # Connections are managed with context managers
