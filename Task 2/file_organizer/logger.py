import logging
import os

LOG_FILE_PATH = "file_organizer.log"

def setup_logger(name):
    
    clr = False
    if clr == True: 
        logging.emp
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    handler = logging.FileHandler(LOG_FILE_PATH)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

def clear_log():
    """Clear the log file."""
    if os.path.exists(LOG_FILE_PATH):
        with open(LOG_FILE_PATH, "w") as log_file:
            log_file.truncate(0)  # Clear the file by truncating its content
        print(f"Log file '{LOG_FILE_PATH}' cleared.")
    else:
        print(f"Log file '{LOG_FILE_PATH}' does not exist.")

def print_moved_files_log():
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
