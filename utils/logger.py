import logging
import os

class Logger:
    """
    Handles logging for the application.
    """

    def __init__(self, log_file="logs/app.log"):
        """
        Initializes the logger and sets up the file handler.

        Args:
            log_file (str): Path to the log file.
        """
        # Ensure the directory for the log file exists
        log_dir = os.path.dirname(log_file)
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)  # Create the directory if it doesn't exist

        # Configure the logger
        self.logger = logging.getLogger("PasswordManagerLogger")
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)

        # Set log format
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

    def info(self, message):
        """Logs an info-level message."""
        self.logger.info(message)

    def error(self, message):
        """Logs an error-level message."""
        self.logger.error(message)

    def warning(self, message):
        """Logs a warning-level message."""
        self.logger.warning(message)

    def debug(self, message):
        self.logger.debug(message)
