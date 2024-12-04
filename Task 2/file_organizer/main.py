import os
from file_organizer.file_sorter import FileOrganizer
from file_organizer.logger import setup_logger, clear_log, print_moved_files_log
from file_organizer.interface import display_menu
from file_organizer.config import FILE_TYPE_MAP



def main():
    # Set up logger
    organize = FileOrganizer()
    logger = setup_logger("file_organizer")
    print("Welcome to the File Organizer!")
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            directory = input("\nEnter the directory to organize: ").strip()
            try:
                organize.organize_files(directory, logger)
                print("File organization completed successfully.")
            except Exception as e:
                logger.error(f"An error occurred: {e}")
                print(f"Error: {e}")
            
        elif choice == "2":
            print("\nCurrent File Categories:")
            for ext, fld in FILE_TYPE_MAP.items():
                print(f"{ext}: {fld}")

            extension = input("\nEnter the file extension to register (e.g., .md, .csv): ").strip()
            folder = input(f"Enter the folder name for files with the '{extension}' extension: ").strip()
            organize.add_new_file_type(extension, folder)
        
        elif choice == "3": 
            print("\nCurrent File Categories:")
            for ext, folder in FILE_TYPE_MAP.items():
                print(f"{ext}: {folder}")
        elif choice == "4":
            print_moved_files_log()
        elif choice == "5":
            clear_log()
        elif choice =="6":
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    

if __name__ == "__main__":
    main()
