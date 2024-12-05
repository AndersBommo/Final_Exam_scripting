import pytest
from unittest.mock import patch, MagicMock, call
import os
import shutil
from file_organizer.file_sorter import FileOrganizer
from file_organizer.logger import File_logger
from file_organizer.config import FILE_TYPE_MAP

LOG_FILE_PATH = "file_organizer.log"

@pytest.fixture
def setup_test_environment():
    """Set up mock data and objects for testing."""
    organizer = FileOrganizer()
    filelogg = File_logger()
    logger = filelogg.setup_logger("file_organizer")  # Use the actual logger
    test_directory = "test_directory"
    test_file_map = {
        ".txt": "TextFiles",
        ".jpg": "Images",
        ".csv": "Data",
        "default": "OtherFiles",
    }
    original_file_type_map = FILE_TYPE_MAP.copy()

    # Mock the FILE_TYPE_MAP during tests
    FILE_TYPE_MAP.update(test_file_map)

    # Create a test directory
    os.makedirs(test_directory, exist_ok=True)

    yield organizer, filelogg, logger, test_directory, original_file_type_map

    # Teardown: Restore the original state after the test
    FILE_TYPE_MAP.clear()
    FILE_TYPE_MAP.update(original_file_type_map)

    # Remove the test directory
    if os.path.exists(test_directory):
        shutil.rmtree(test_directory)

    # Properly close the logger's handlers to release the log file
    for handler in logger.handlers[:]:
        handler.close()
        logger.removeHandler(handler)

    # Remove the log file if it's not in use
    if os.path.exists(LOG_FILE_PATH):
        try:
            os.remove(LOG_FILE_PATH)
        except PermissionError:
            print(f"Error: Could not delete the log file {LOG_FILE_PATH} because it is still in use.")

@pytest.fixture
def mock_logger():
    """Fixture to create a mock logger."""
    logger = MagicMock()
    return logger


def test_organize_files_with_logger(setup_test_environment, mock_logger):
    """Test file organization with logger integration."""
    organizer, filelogg, logger, test_directory, _ = setup_test_environment

    # Mock os.walk to simulate files in the directory
    with patch("os.walk") as mock_walk, patch("os.makedirs") as mock_makedirs, patch("shutil.move") as mock_move:
        mock_walk.return_value = [
            (test_directory, [], ["file1.txt", "file2.jpg", "file3.csv"]),
        ]

        # Call organize_files
        organizer.organize_files(test_directory, logger)

        # Assert that folders were created
        mock_makedirs.assert_has_calls([
            call(os.path.join(test_directory, "TextFiles"), exist_ok=True),
            call(os.path.join(test_directory, "Images"), exist_ok=True),
            call(os.path.join(test_directory, "Data"), exist_ok=True),
            call(os.path.join(test_directory, "OtherFiles"), exist_ok=True),
        ], any_order=True)

        # Assert that files were moved
        mock_move.assert_has_calls([
            call(os.path.join(test_directory, "file1.txt"), os.path.join(test_directory, "TextFiles", "file1.txt")),
            call(os.path.join(test_directory, "file2.jpg"), os.path.join(test_directory, "Images", "file2.jpg")),
            call(os.path.join(test_directory, "file3.csv"), os.path.join(test_directory, "Data", "file3.csv")),
        ], any_order=True)

        # Assert logger logged the file moves
        with open(LOG_FILE_PATH, "r") as log_file:
            log_content = log_file.read()
            assert "Moved file1.txt to TextFiles." in log_content
            assert "Moved file2.jpg to Images." in log_content
            assert "Moved file3.csv to Data." in log_content


def test_clear_log(setup_test_environment):
    """Test the clear_log function."""
    filelogg = setup_test_environment[1]
    # Write dummy content to the log file
    with open(LOG_FILE_PATH, "w") as log_file:
        log_file.write("Dummy log content.\n")

    # Call clear_log
    filelogg.clear_log()

    # Assert the log file is cleared
    assert os.path.exists(LOG_FILE_PATH)
    with open(LOG_FILE_PATH, "r") as log_file:
        assert log_file.read() == ""


def test_print_moved_files_log(setup_test_environment):
    """Test the print_moved_files_log function."""
    filelogg = setup_test_environment[1]
    # Write sample "Moved" log entries
    with open(LOG_FILE_PATH, "w") as log_file:
        log_file.write("2023-12-04 10:00:00 - INFO - Moved file1.txt to TextFiles.\n")
        log_file.write("2023-12-04 10:01:00 - INFO - Moved file2.jpg to Images.\n")

    # Capture print output
    with patch("builtins.print") as mock_print:
        filelogg.print_moved_files_log()

    # Assert the moved files log is printed
    mock_print.assert_any_call("\nMoved Files Log:")
    mock_print.assert_any_call("file1.txt to TextFiles.")
    mock_print.assert_any_call("file2.jpg to Images.")
