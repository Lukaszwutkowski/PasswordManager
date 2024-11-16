import logging

class Logger:
    """
    Handles logging for the application.
    """

    def __init__(self, log_file="logs/app.log"):
        """
        Initializes the Logger and sets up the logging configuration.

        Args:
            log_file (str): Path to the log file.
        """
        self.logger = logging.getLogger("PasswordManagerLogger")
        self.logger.setLevel(logging.DEBUG)
        file_handler = logging.FileHandler(log_file)
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
