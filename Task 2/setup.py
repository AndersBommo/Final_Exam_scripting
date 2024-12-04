# setup.py
from setuptools import setup, find_packages
# Define the package setup configuration
setup(
    name='file_organizer',  # Name of the package
    version='1.0',  # Version of the package
    packages=find_packages(),  # Automatically find and include all packages in the directory
    description='A Python package for organizing files',  # Brief description of the package
    install_requires=[],  # Dependencies for the package (empty here since there are none)
    
    # Define the entry point for command-line usage
    entry_points={
    'console_scripts': [
        'file_organizer=file_organizer.main:main',  # Ensure the path matches the actual structure
        ]
    }
    
)
