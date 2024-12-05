# ACIT 4420 Scripting Exam Project

This repository contains the project submission for the ACIT 4420 Scripting Exam. The project is divided into two distinct parts, each addressing a unique problem using Python scripting:

1. **Tarjan Planner**  
2. **File Organizer**

---

## 1. Tarjan Planner

The **Tarjan Planner** is a Python-based program designed to calculate optimal travel routes for multiple locations. It allows users to select preferences for minimizing travel time, cost, or the number of transfers, while also incorporating different modes of transportation such as buses, trains, bicycles, and walking.

### Key Features:
- **Route Optimization:** Computes the best route based on user preferences using graph-based algorithms.  
- **Transport Modes:** Evaluates various transport modes dynamically based on distance and user-defined priorities.  
- **Interactive Interface:** Provides a user-friendly menu for inputting locations, selecting preferences, and saving routes.  
- **Route Visualization:** Generates visual plots of routes with detailed transport mode breakdowns.  

This program is ideal for scenarios requiring personalized route planning for multiple destinations.  

---

## 2. File Organizer

The **File Organizer** is a utility program designed to automate the organization of files within a directory. It categorizes files based on their extensions and moves them into predefined or user-defined folders, simplifying directory management tasks.

### Key Features:
- **Automatic Categorization:** Sorts files into folders such as `Documents`, `Images`, and `Videos` based on their extensions.  
- **Dynamic Folder Management:** Allows users to define new file types and corresponding folders dynamically.  
- **Logging:** Maintains a detailed log of file movements for traceability.  
- **Cross-Platform Compatibility:** Works seamlessly across different operating systems, including Windows, macOS, and Linux.  

This program is a practical tool for users looking to maintain organized and clutter-free directories.

---

### Repository Structure:
```
ACIT_4420_scripting_exam
├── .gitattributes
├── README.md
├── file_organizer.log
├── task1
│   ├── build
│   ├── exported_routes
│   ├── tarjan_planner
│   │   ├── __init__.py
│   │   ├── __main__.py
│   │   ├── distance_calculator.py
│   │   ├── interface.py
│   │   ├── main.py
│   │   ├── route_bruteforce.py
│   │   └── time_logger.py
│   ├── tarjan_planner.egg-info
│   ├── tests
│   └── setup.py
├── task2
│    ├── build
│    ├── file_organizer
│    │   ├── config.py
│    │   ├── __init__.py
│    │   ├── __main__.py
│    │   ├── config.py
│    │   ├── file_sorter.py
│    │   ├── interface.py
│    │   ├── logger.py
│    │   └── main.py
│    ├── file_organizer.egg-info
│    ├── file_organizer.log
│    └── setup.py

