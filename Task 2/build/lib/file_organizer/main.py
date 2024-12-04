import os
from file_organizer.file_sorter import organize_files
from file_organizer.logger import setup_logger, clear_log
from file_organizer.interface import *
from file_organizer.config import register_file_type, FILE_TYPE_MAP, add_new_file_type



def main():
    # Set up logger

    logger = setup_logger("file_organizer")
    print("Welcome to the File Organizer!")
    while True:
        display_menu()
        choice = input("\nEnter your choice (1-5): ").strip()
        
        if choice == "1":
            organize_files_menu(logger)
        elif choice == "2":
            add_file_type_menu()
        elif choice == "3":
            clear_log()
        elif choice == "4":
            print("\nCurrent File Categories:")
            for ext, folder in FILE_TYPE_MAP.items():
                print(f"{ext}: {folder}")
        elif choice =="5":
            print("Exiting the program. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")

    # Allow user to dynamically add file types
    

    try:
        # Directory to organize
        directory = input("Enter the directory to organize: ").strip()
        if not os.path.exists(directory):
            raise FileNotFoundError(f"The directory {directory} does not exist.")
        
        # Organize files
        organize_files(directory, logger)
        logger.info("File organization completed successfully.")
    except Exception as e:
        logger.error(f"An error occurred: {e}")



if __name__ == "__main__":
    main()
