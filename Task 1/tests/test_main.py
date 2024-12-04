import unittest
from unittest.mock import patch
from tarjan_planner.interface import UserInterface

class TestUserInterface(unittest.TestCase):

    @patch('builtins.input', return_value="1")
    def test_menu_valid_option(self, mock_input):
        """Test the menu method when a valid option is selected."""
        user_input = UserInterface.menu()
        self.assertEqual(user_input, "1")
        mock_input.assert_called_once()

    @patch('builtins.input', return_value="99")
    def test_menu_invalid_option(self, mock_input):
        """Test the menu method with an invalid option."""
        user_input = UserInterface.menu()
        self.assertEqual(user_input, "99")
        mock_input.assert_called_once()

    @patch('builtins.input', side_effect=["1"])
    def test_get_user_preference_valid_time(self, mock_input):
        """Test the get_user_preference method when 'time' is selected."""
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'time')
        mock_input.assert_called()

    @patch('builtins.input', side_effect=["2"])
    def test_get_user_preference_valid_cost(self, mock_input):
        """Test the get_user_preference method when 'cost' is selected."""
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'cost')
        mock_input.assert_called()

    @patch('builtins.input', side_effect=["3"])
    def test_get_user_preference_valid_transfers(self, mock_input):
        """Test the get_user_preference method when 'transfers' is selected."""
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'transfers')
        mock_input.assert_called()

    @patch('builtins.input', side_effect=["4", "5", "3"])
    def test_get_user_preference_invalid_input(self, mock_input):
        """Test the get_user_preference method when invalid input is provided."""
        preference = UserInterface.get_user_preference()
        self.assertEqual(preference, 'transfers')  # After two invalid inputs, it should choose '3' (transfers)
        self.assertEqual(mock_input.call_count, 3)

    @patch('builtins.print')
    def test_print_route_information(self, mock_print):
        """Test the print_route_information method to ensure the correct output format."""
        route = ['tarjan_home', 'Relative_1', 'Relative_2']
        distance = 10.0
        preference = 'time'
        route_modes = [('tarjan_home', 'Relative_1', 'bus'), ('Relative_1', 'Relative_2', 'train')]

        UserInterface.print_route_information(route, distance, preference, route_modes)

        # Check that the correct print statements were called
        mock_print.assert_any_call("Optimal route based on time:")
        mock_print.assert_any_call("Distance: 10.00 km")
        mock_print.assert_any_call("\nTransport Modes:")
        mock_print.assert_any_call("tarjan_home -> Relative_1: bus")
        mock_print.assert_any_call("Relative_1 -> Relative_2: train")


if __name__ == "__main__":
    unittest.main()
