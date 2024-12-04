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
