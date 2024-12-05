import unittest
from unittest.mock import patch, MagicMock, call
import os
import shutil
from file_organizer.file_sorter import FileOrganizer
from file_organizer.logger import File_logger
#setup_logger, clear_log, print_moved_files_log
from file_organizer.config import FILE_TYPE_MAP

LOG_FILE_PATH = "file_organizer.log"

class TestFileSorterWithLogger(unittest.TestCase):

    def setUp(self):
        """Set up mock data and objects for testing."""
        self.organizer = FileOrganizer()
        self.filelogg = File_logger()
        self.logger = self.filelogg.setup_logger("file_organizer")  # Use the actual logger
        self.test_directory = "test_directory"
        self.test_file_map = {
            ".txt": "TextFiles",
            ".jpg": "Images",
            ".csv": "Data",
            "default": "OtherFiles",
        }
        self.original_file_type_map = FILE_TYPE_MAP.copy()

        # Mock the FILE_TYPE_MAP during tests
        FILE_TYPE_MAP.update(self.test_file_map)

        # Create a test directory
        os.makedirs(self.test_directory, exist_ok=True)

    def tearDown(self):
        """Clean up after tests."""
        # Restore original FILE_TYPE_MAP
        FILE_TYPE_MAP.clear()
        FILE_TYPE_MAP.update(self.original_file_type_map)

        # Remove the test directory
        if os.path.exists(self.test_directory):
            shutil.rmtree(self.test_directory)

        # Properly close the logger's handlers to release the log file
        for handler in self.logger.handlers[:]:
            handler.close()
            self.logger.removeHandler(handler)

        # Remove the log file
        if os.path.exists(LOG_FILE_PATH):
            os.remove(LOG_FILE_PATH)

    @patch("os.makedirs")
    @patch("os.walk")
    @patch("shutil.move")
    def test_organize_files_with_logger(self, mock_move, mock_walk, mock_makedirs):
        """Test file organization with logger integration."""
        # Mock os.walk to simulate files in the directory
        mock_walk.return_value = [
            (self.test_directory, [], ["file1.txt", "file2.jpg", "file3.csv"]),
        ]

        # Call organize_files
        self.organizer.organize_files(self.test_directory, self.logger)

        # Assert that folders were created
        mock_makedirs.assert_has_calls([
            call(os.path.join(self.test_directory, "TextFiles"), exist_ok=True),
            call(os.path.join(self.test_directory, "Images"), exist_ok=True),
            call(os.path.join(self.test_directory, "Data"), exist_ok=True),
            call(os.path.join(self.test_directory, "OtherFiles"), exist_ok=True),
        ], any_order=True)

        # Assert that files were moved
        mock_move.assert_has_calls([
            call(os.path.join(self.test_directory, "file1.txt"), os.path.join(self.test_directory, "TextFiles", "file1.txt")),
            call(os.path.join(self.test_directory, "file2.jpg"), os.path.join(self.test_directory, "Images", "file2.jpg")),
            call(os.path.join(self.test_directory, "file3.csv"), os.path.join(self.test_directory, "Data", "file3.csv")),
        ], any_order=True)

        # Assert logger logged the file moves
        with open(LOG_FILE_PATH, "r") as log_file:
            log_content = log_file.read()
            self.assertIn("Moved file1.txt to TextFiles.", log_content)
            self.assertIn("Moved file2.jpg to Images.", log_content)
            self.assertIn("Moved file3.csv to Data.", log_content)

    def test_clear_log(self):
        """Test the clear_log function."""
        # Write dummy content to the log file
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.write("Dummy log content.\n")

        # Call clear_log
        self.filelogg.clear_log()

        # Assert the log file is cleared
        self.assertTrue(os.path.exists(LOG_FILE_PATH))
        with open(LOG_FILE_PATH, "r") as log_file:
            self.assertEqual(log_file.read(), "")

    def test_print_moved_files_log(self):
        """Test the print_moved_files_log function."""
        # Write sample "Moved" log entries
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.write("2023-12-04 10:00:00 - INFO - Moved file1.txt to TextFiles.\n")
            log_file.write("2023-12-04 10:01:00 - INFO - Moved file2.jpg to Images.\n")

        # Capture print output
        with patch("builtins.print") as mock_print:
            self.filelogg.print_moved_files_log()

        # Assert the moved files log is printed
        mock_print.assert_any_call("\nMoved Files Log:")
        mock_print.assert_any_call("file1.txt to TextFiles.")
        mock_print.assert_any_call("file2.jpg to Images.")