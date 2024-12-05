# File Organizer

The **File Organizer** is a Python-based utility program designed to automate the process of organizing files within a directory. It categorizes files based on their extensions and moves them into predefined or user-defined folders, making directory management simpler and more efficient.

---

## Features

- **Automatic Categorization:** Organizes files into categories such as `Documents`, `Images`, and `Videos` based on their extensions.  
- **Dynamic Category Management:** Allows users to define new file types and corresponding folders.  
- **Logging:** Maintains a detailed log of file movements for traceability and debugging.  
- **Cross-Platform Compatibility:** Works seamlessly on Windows, macOS, and Linux.  

---

## Installation

1. Ensure you have Python 3.8 or higher installed on your system.
2. Navigate to the `task2` directory in the project:
   ```bash
   cd Task 2

   pip install -e .
    ```


## Usage
```bash 
python -m file_organizer
```

## Directory Structure

```
├──  task2
|   ├──  build
|   ├──  file_organizer
|   |   ├──  config.py
|   |   ├──  __init__.py
|   |   ├──  __main__.py
|   |   ├──  file_sorter.py
|   |   ├──  interface.py
|   |   ├──  logger.py
|   |   └── main.py
|   ├──  file_organizer.egg-info
|   ├──  file_organizer.log
|   └── setup.py

file_organizer/: Contains the core logic for the application.
__main__.py: Entry point for running the program.
file_sorter.py: Implements file sorting and movement logic.
config.py: Defines the mapping of file extensions to folder categories.
interface.py: Provides a user-friendly menu for interaction.
logger.py: Handles logging of file movements and log management.
file_organizer.log: Log file for tracking file organization actions