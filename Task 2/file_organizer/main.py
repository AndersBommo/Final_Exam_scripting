# main.py
import os
from file_organizer.file_sorter import FileOrganizer
from file_organizer.logger import File_logger
#setup_logger, clear_log, print_moved_files_log
from file_organizer.interface import UserInterface
from file_organizer.config import FILE_TYPE_MAP


def main():
    # Set up logger
    organize = FileOrganizer()
    interface = UserInterface()
    logfile = File_logger()
    logg = logfile.setup_logger("file_organizer")
    
    print("Welcome to the File Organizer!")

    max_retries = 3  # Set the maximum number of invalid attempts
    invalid_attempts = 0  # Counter to track invalid choices

    while True:
        try:
            choice = interface.display_menu()
            if choice == "1":  # Organize files in a directory
                directory = input("\nEnter the directory to organize: ").strip()
                if not os.path.isdir(directory):
                    print(f"Error: '{directory}' is not a valid directory.")
                    logfile.error(f"Invalid directory provided: {directory}")
                    continue

                try:
                    organize.organize_files(directory, logg)
                    print("File organization completed successfully.")
                except Exception as e:
                    logfile.error(f"An error occurred while organizing files: {e}")
                    print(f"Error: {e}")

            elif choice == "2":  # Register a new file type
                print("\nCurrent File Categories:")
                for ext, fld in FILE_TYPE_MAP.items():
                    print(f"{ext}: {fld}")

                extension = input("\nEnter the file extension to register (e.g., .md, .csv): ").strip()
                if not extension.startswith("."):
                    print("Error: File extension must start with a dot (e.g., '.md').")
                    logfile.error(f"Invalid file extension entered: {extension}")
                    continue

                folder = input(f"Enter the folder name for files with the '{extension}' extension: ").strip()
                if not folder:
                    print("Error: Folder name cannot be empty.")
                    logfile.error(f"Empty folder name provided for extension: {extension}")
                    continue

                try:
                    organize.add_new_file_type(extension, folder)
                    print(f"File type '{extension}' registered under '{folder}'.")
                except Exception as e:
                    logfile.error(f"Error registering new file type: {e}")
                    print(f"Error: {e}")

            elif choice == "3":  # Display file type mappings
                print("\nCurrent File Categories:")
                for ext, folder in FILE_TYPE_MAP.items():
                    print(f"{ext}: {folder}")

            elif choice == "4":  # Print moved files log
                try:
                    logg.print_moved_files_log()
                except FileNotFoundError:
                    print("Log file not found. No files have been moved yet.")
                    logfile.warning("Attempted to print a non-existent log file.")
                except Exception as e:
                    logfile.error(f"Error while printing moved files log: {e}")
                    print(f"Error: {e}")

            elif choice == "5":  # Clear log
                try:
                    logg.clear_log()
                    print("Log cleared successfully.")
                except Exception as e:
                    logfile.error(f"Error clearing the log: {e}")
                    print(f"Error: {e}")

            elif choice == "6":  # Exit program
                print("Exiting the program. Goodbye!")
                break

            else:
                invalid_attempts += 1
                if invalid_attempts >= max_retries:
                    print("Too many invalid attempts. Exiting the program.")
                    break
                else:
                    print(f"Invalid choice. You have {max_retries - invalid_attempts} attempts left.")
                    logfile.warning(f"Invalid menu choice entered: {choice}")

        except Exception as e:
            print(f"Error: {e}")
            logfile.error(f"Unexpected error: {e}")
            break



if __name__ == "__main__":
    main()
