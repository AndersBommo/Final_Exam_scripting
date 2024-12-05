#interface.py
class UserInterface: 
    def display_menu(self):

        """Display the main menu options."""
        print("\n--- File Organizer Menu ---")
        print("1. Organize files in a directory")
        print("2. Add a new file type category")
        print("3. Show Existing file types")
        print("4. Print log")
        print("5. Clear the log")
        print("6. Exit")
        userinput = input()
        return userinput
