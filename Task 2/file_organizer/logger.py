import logging
import os

LOG_FILE_PATH = "file_organizer.log"

class File_logger:
    def setup_logger(self, name):
        # Set up the logger instance
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)

        # Check if we need to clear the log file before setting it up
        clr = False  # Set to True if you want to clear the log file on setup
        if clr:
            self.clear_log()  # Clear the log if needed

        handler = logging.FileHandler(LOG_FILE_PATH)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def clear_log(self):
        """Clear the log file."""
        try:
            if os.path.exists(LOG_FILE_PATH):
                # Use "with open" for safe file handling
                with open(LOG_FILE_PATH, "w") as log_file:
                    log_file.write("")  # Clear the file by writing an empty string
                print(f"Log file '{LOG_FILE_PATH}' cleared.")
            else:
                print(f"Log file '{LOG_FILE_PATH}' does not exist.")
        except Exception as e:
            print(f"An error occurred while clearing the log: {e}")

    def print_moved_files_log(self):
        """Print the log entries related to moved files, showing only file and destination folder."""
        if not os.path.exists(LOG_FILE_PATH):
            print(f"Log file '{LOG_FILE_PATH}' does not exist.")
            return

        if os.stat(LOG_FILE_PATH).st_size == 0:
            print(f"Log file '{LOG_FILE_PATH}' is empty.")
            return
        
        print("\nMoved Files Log:")
        with open(LOG_FILE_PATH, "r") as log_file:
            for line in log_file:
                # Check if the line contains 'Moved' (case insensitive)
                if "moved" in line.lower():
                    # Split the line to extract the moved file and destination folder
                    parts = line.split(" - INFO - Moved ")
                    if len(parts) > 1:
                        file_and_folder = parts[1].strip()
                        print(file_and_folder)
