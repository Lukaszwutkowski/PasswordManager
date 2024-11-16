import os

class FileManager:
    """
    Handles file-related operations, such as reading and writing files.
    """

    @staticmethod
    def read_file(file_path, mode="r"):
        """
        Reads the content of a file.

        Args:
            file_path (str): Path to the file.
            mode (str): Mode to open the file. Default is "r" (read).

        Returns:
            str or bytes: The content of the file.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")
        with open(file_path, mode) as file:
            return file.read()

    @staticmethod
    def write_file(file_path, content, mode="w"):
        """
        Writes content to a file.

        Args:
            file_path (str): Path to the file.
            content (str or bytes): The content to write.
            mode (str): Mode to open the file. Default is "w" (write).
        """
        with open(file_path, mode) as file:
            file.write(content)

    @staticmethod
    def delete_file(file_path):
        """
        Deletes a file if it exists.

        Args:
            file_path (str): Path to the file.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
