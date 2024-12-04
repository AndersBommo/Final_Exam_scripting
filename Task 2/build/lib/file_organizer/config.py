FILE_TYPE_MAP = {
    ".jpg": "Images",
    ".jpeg": "Images",
    ".png": "Images",
    ".gif": "Images",
    ".pdf": "Documents",
    ".docx": "Documents",
    ".xlsx": "Documents",
    ".txt": "Text",
    # Default fallback
    "default": "Others",
}



def add_new_file_type():
    """Prompt user to add a new file type."""
    while True:
        print("\nCurrent File Categories:")
        for ext, folder in FILE_TYPE_MAP.items():
            print(f"{ext}: {folder}")
        
        extension = input("\nEnter the file extension to register (e.g., .md, .csv): ").strip()
        folder = input(f"Enter the folder name for files with the '{extension}' extension: ").strip()
        
        if not extension.startswith("."):
            print("Error: File extensions should start with a dot (e.g., .txt).")
            continue
        
        if extension.lower() in FILE_TYPE_MAP:
            print(f"'{extension}' is already registered under '{FILE_TYPE_MAP[extension.lower()]}'.")
        else:
            # Register the new file type
            register_file_type(extension, folder)
            print(f"Successfully registered '{extension}' under the folder '{folder}'!")
        
        # Ask if the user wants to add another type
        more = input("Do you want to add another file type? (y/n): ").strip().lower()
        if more != 'y':
            break

def register_file_type(extension, folder):
    """Register new file types dynamically."""
    FILE_TYPE_MAP[extension.lower()] = folder
