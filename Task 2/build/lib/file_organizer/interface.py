
from file_organizer.config import FILE_TYPE_MAP, register_file_type
from file_organizer.file_sorter import organize_files


def display_menu():
    """Display the main menu options."""
    print("\n--- File Organizer Menu ---")
    print("1. Organize files in a directory")
    print("2. Add a new file type category")
    print("3. Clear the log file")
    print("4. Show Existing file types")
    print("5. Show Existing file types")

def organize_files_menu(logger):
    """Prompt user to organize files in a directory."""
    directory = input("\nEnter the directory to organize: ").strip()
    try:
        organize_files(directory, logger)
        print("File organization completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")
        print(f"Error: {e}")

def add_file_type_menu():
    """Prompt user to add a new file type category."""
    extension = input("\nEnter the file extension to register (e.g., .md, .csv): ").strip()
    folder = input(f"Enter the folder name for files with the '{extension}' extension: ").strip()
    
    if not extension.startswith("."):
        print("Error: File extensions should start with a dot (e.g., .txt).")
        return
    
    if extension.lower() in FILE_TYPE_MAP:
        print(f"'{extension}' is already registered under '{FILE_TYPE_MAP[extension.lower()]}'.")
    else:
        register_file_type(extension, folder)
        print(f"Successfully registered '{extension}' under the folder '{folder}'!")
