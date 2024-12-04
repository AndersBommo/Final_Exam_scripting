import unittest
from unittest.mock import patch
from tarjan_planner.interface import UserInterface

class TestUserInterface(unittest.TestCase):

    @patch('builtins.input', side_effect=["1", "2", "3", "7"])  # Mock user inputs for menu
    def test_menu(self, mock_input):
        """Test the menu function for correct user input handling."""
        # Test for menu option 1
        choice = UserInterface.menu()
        self.assertEqual(choice, "1")

        # Test for menu option 2
        choice = UserInterface.menu()
        self.assertEqual(choice, "2")

        # Test for menu option 3
        choice = UserInterface.menu()
        self.assertEqual(choice, "3")

        # Test for menu option 7 (Exit)
        choice = UserInterface.menu()
        self.assertEqual(choice, "7")

    @patch('builtins.input', side_effect=["1", "2", "3", "invalid", "2"])  # Mock user inputs for preference
    def test_get_user_preference(self, mock_input):
        """Test the get_user_preference function for correct input handling."""
        # Test for valid input '1' (time)
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'time')

        # Test for valid input '2' (cost)
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'cost')

        # Test for valid input '3' (transfers)
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'transfers')

        # Test for invalid input (should retry and accept valid input after that)
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'cost')  # User should eventually choose 'cost'

    @patch('builtins.print')  # Mock the print function to capture printed outputs
    def test_print_route_information(self, mock_print):
        """Test the print_route_information function for correct output."""
        # Sample data for the test
        route = ["tarjan_home", "Relative_1", "Relative_2"]
        distance = 10.5
        preference = "time"
        route_modes = [("tarjan_home", "Relative_1", "bus"), ("Relative_1", "Relative_2", "train")]

        # Call the method to print route information
        UserInterface.print_route_information(route, distance, preference, route_modes)

        # Check that the correct information is printed
        mock_print.assert_any_call(f"Optimal route based on {preference}:")
        mock_print.assert_any_call(f"Distance: {distance:.2f} km")
        mock_print.assert_any_call("\nTransport Modes:")
        mock_print.assert_any_call("tarjan_home -> Relative_1: bus")
        mock_print.assert_any_call("Relative_1 -> Relative_2: train")

if __name__ == "__main__":
    unittest.main()
