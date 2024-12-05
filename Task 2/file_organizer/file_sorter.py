#file_sorter.py
import os
import shutil
from file_organizer.config import FILE_TYPE_MAP

class FileOrganizer: 
    def __init__(self) -> None:
        pass
    def organize_files(self,directory, logger):
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


    def add_new_file_type(self, extension, folder):
        """Prompt user to add a new file type."""
        while True:
            # Print current file categories BEFORE adding a new file type
            print("\nCurrent File Categories:")
            for ext, fld in FILE_TYPE_MAP.items():
                print(f"{ext}: {fld}")
            
            if not extension.startswith("."):
                print("Error: File extensions should start with a dot (e.g., .txt).")
                continue
            
            # Check if the extension is already registered
            if extension.lower() in FILE_TYPE_MAP:
                print(f"'{extension}' is already registered under '{FILE_TYPE_MAP[extension.lower()]}'.")
            else:
                # Register the new file type with the folder
                FILE_TYPE_MAP[extension.lower()] = folder
                print(f"Successfully registered '{extension}' under the folder '{folder}'!")
            
            # Print updated file categories AFTER adding the new one
            print("\nUpdated File Categories:")
            for ext, fld in FILE_TYPE_MAP.items():
                print(f"{ext}: {fld}")
            
            # Ask if the user wants to add another type
            more = input("Do you want to add another file type? (y/n): ").strip().lower()
            if more != 'y':
                break
            else:
                # Ask for the new extension and folder for the next entry
                extension = input("\nEnter the file extension to register (e.g., .md, .csv): ").strip()
                folder = input(f"Enter the folder name for files with the '{extension}' extension: ").strip()





    