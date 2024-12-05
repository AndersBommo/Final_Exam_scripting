import pytest
from unittest.mock import patch
from tarjan_planner.interface import UserInterface


# Test the menu method for valid input handling
@pytest.mark.parametrize("input_value, expected_choice", [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("7", "7")
])
@patch('builtins.input')
def test_menu_valid_option(mock_input, input_value, expected_choice):
    """Test the menu method when a valid option is selected."""
    mock_input.side_effect = [input_value]
    user_input = UserInterface.menu()
    assert user_input == expected_choice


# Test the menu method for invalid input handling
@patch('builtins.input', return_value="99")
def test_menu_invalid_option(mock_input):
    """Test the menu method with an invalid option."""
    user_input = UserInterface.menu()
    assert user_input == "99"
    mock_input.assert_called_once()


# Test the get_user_preference method for valid input (time)
@patch('builtins.input', side_effect=["1"])
def test_get_user_preference_valid_time(mock_input):
    """Test the get_user_preference method when 'time' is selected."""
    preference = UserInterface.get_user_preference()
    assert preference == 'time'
    mock_input.assert_called()


# Test the get_user_preference method for valid input (cost)
@patch('builtins.input', side_effect=["2"])
def test_get_user_preference_valid_cost(mock_input):
    """Test the get_user_preference method when 'cost' is selected."""
    preference = UserInterface.get_user_preference()
    assert preference == 'cost'
    mock_input.assert_called()


# Test the get_user_preference method for valid input (transfers)
@patch('builtins.input', side_effect=["3"])
def test_get_user_preference_valid_transfers(mock_input):
    """Test the get_user_preference method when 'transfers' is selected."""
    preference = UserInterface.get_user_preference()
    assert preference == 'transfers'
    mock_input.assert_called()


# Test the get_user_preference method for invalid input handling
@patch('builtins.input', side_effect=["4", "5", "3"])
def test_get_user_preference_invalid_input(mock_input):
    """Test the get_user_preference method when invalid input is provided."""
    preference = UserInterface.get_user_preference()
    assert preference == 'transfers'  # After two invalid inputs, it should choose '3' (transfers)
    assert mock_input.call_count == 3


# Test the print_route_information method for correct output
@patch('builtins.print')
def test_print_route_information(mock_print):
    """Test the print_route_information method to ensure the correct output format."""
    route = ['tarjan_home', 'Relative_1', 'Relative_2']
    distance = 10.0
    preference = 'time'
    route_modes = [('tarjan_home', 'Relative_1', 'bus'), ('Relative_1', 'Relative_2', 'train')]
    total_distance = 20.5  # Add a value for total_distance

    # Call the method to print route information
    UserInterface.print_route_information(route, distance, preference, route_modes, total_distance)

    # Check that the correct print statements were called
    mock_print.assert_any_call("Optimal route based time:")  # Fixed expected string
    mock_print.assert_any_call("Route: ['tarjan_home', 'Relative_1', 'Relative_2']")
    mock_print.assert_any_call("Total Distance: 20.50 km")
    mock_print.assert_any_call("time spent traveling: 600.00 minutes")
    mock_print.assert_any_call("\nTransport Modes:")
    mock_print.assert_any_call("tarjan_home -> Relative_1: bus")
    mock_print.assert_any_call("Relative_1 -> Relative_2: train")
