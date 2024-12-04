import os
import shutil
from file_organizer.config import FILE_TYPE_MAP

def organize_files(directory, logger):
    for folder in FILE_TYPE_MAP.values():
        os.makedirs(os.path.join(directory, folder), exist_ok=True)

    for root, _, files in os.walk(directory):
        for file in files:
            file_ext = os.path.splitext(file)[-1].lower()
            folder = FILE_TYPE_MAP.get(file_ext, FILE_TYPE_MAP["default"])
            dest_path = os.path.join(directory, folder, file)
            
            try:
                shutil.move(os.path.join(root, file), dest_path)
                logger.info(f"Moved {file} to {folder}.")
            except Exception as e:
                logger.error(f"Failed to move {file}: {e}")

