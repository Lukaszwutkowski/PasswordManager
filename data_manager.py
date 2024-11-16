import sqlite3

class DataManager:
    """
    Manages data persistence using SQLite for storing passwords.
    """

    def __init__(self, db_path="data/passwords.db"):
        """
        Initializes the DataManager and creates the database and table if they do not exist.

        Args:
            db_path (str): Path to the SQLite database file.
        """
        self.db_path = db_path
        self.connection = None
        self._create_table()

    def _create_connection(self):
        """
        Creates or returns an existing connection to the SQLite database.

        Returns:
            sqlite3.Connection: A connection object to the SQLite database.
        """
        if not self.connection:
            self.connection = sqlite3.connect(self.db_path)
        return self.connection

    def _create_table(self):
        """
        Creates the passwords table in the database if it does not already exist.
        """
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                website TEXT NOT NULL,
                email TEXT NOT NULL,
                password TEXT NOT NULL
            )
        """)
        conn.commit()

    def save_password(self, website, email, password):
        """
        Saves a password to the database.

        Args:
            website (str): The website name.
            email (str): The email or username.
            password (str): The encrypted password to save.
        """
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            cursor.execute("""
                    INSERT INTO passwords (website, email, password)
                    VALUES (?, ?, ?)
                """, (website, email, password))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error saving password: {str(e)}")
            raise

    def get_passwords(self):
        """
        Retrieves all passwords from the database.

        Returns:
            list of tuples: A list of (website, email, password) entries.
        """
        conn = self._create_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT website, email, password FROM passwords")
            results = cursor.fetchall()  # Pobranie wszystkich danych
            return results
        except sqlite3.Error as e:
            print(f"Error retrieving passwords: {str(e)}")
            raise

    def search_password(self, website):
        """
        Searches for a password in the database by website name.

        Args:
            website (str): The name of the website.

        Returns:
            tuple or None: A tuple (website, email, password) if found, otherwise None.
        """
        conn = self._create_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT website, email, password FROM passwords
            WHERE LOWER(website) = ?
        """, (website.lower(),))  # Porównywanie małych liter w SQL
        return cursor.fetchone()

    def clear_table(self):
        """
        Deletes all entries in the passwords table.
        """
        try:
            conn = self._create_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM passwords")
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error clearing table: {str(e)}")
            raise
        finally:
            conn.close()

    def close(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.connection.close()
            self.connection = None
