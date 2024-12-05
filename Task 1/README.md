# Tarjan Planner

The **Tarjan Planner** is a Python-based route optimization tool designed to calculate the most efficient travel routes based on user preferences. It supports various transport modes (bus, train, bicycle, walking) and provides a user-friendly interface for planning, saving, and visualizing routes.

---

## Features

- **Route Optimization:** Computes the best travel route based on user-defined preferences: minimizing time, cost, or the number of transfers.
- **Transport Modes:** Dynamically selects transport modes based on distance and user priorities.
- **Interactive Menu:** Guides users through the route planning process, including adding or removing locations and viewing saved routes.
- **Route Visualization:** Plots the optimized route with transport mode details.

---

## Installation

1. Ensure you have Python 3.8 or higher installed on your system.
2. Navigate to the `Task 1` directory in the project:
   ```bash
   cd Task 1
   pip install -e .

## Usage

    python -m tarjan_planner


## Directory Structure
```
├── task1 
|   ├── build
|   ├── exported_routes
|   ├── tarjan_planner
|   |   ├── __init__.py
|   |   ├── __main__.py
|   |   ├── distance_calculator.py
|   |   ├── interface.py
|   |   ├── main.py
|   |   ├── route_bruteforce.py
|   |   └── time_logger.py
|   ├── tarjan_planner.egg-info
|   ├── setup.py
|   ├── tests
|   |   ├── test_interface.py
|   |   ├── test_main.py
|   |   └── test_route_planner.py

tarjan_planner.py: Contains the core logic for the application. 
__main__.py: Entry point for running the program.
route_bruteforce.py: Implements route optimization logic.
distance_calculator.py: Calculates distances between locations.
interface.py: Handles user interaction.
time_logger.py: Logs execution times of key operations.
exported_routes/: Directory for saving exported route files.
tests/: Contains unit tests for core modules.




