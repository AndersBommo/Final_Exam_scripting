# setup.py
from setuptools import setup, find_packages
# Define the package setup configuration
setup(
    name='tarjan_planner',  # Name of the package
    version='1.0',  # Version of the package
    packages=find_packages(),  # Automatically find and include all packages in the directory
    description='A Python package for calculating distances',  # Brief description of the package
    install_requires=[],  # Dependencies for the package (empty here since there are none)
    
    # Define the entry point for command-line usage
    entry_points={
        'console_scripts': [
            'tarjan_planner=tarjan_planner.main:main.py',  # Creates a 'morning_greetings' command to run the main() function
        ]
    },
)
