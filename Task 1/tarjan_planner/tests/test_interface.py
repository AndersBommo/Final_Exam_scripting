import pytest
from unittest.mock import patch
from tarjan_planner.interface import UserInterface

# Test the menu function for correct user input handling
@pytest.mark.parametrize("input_value, expected_choice", [
    ("1", "1"),
    ("2", "2"),
    ("3", "3"),
    ("7", "7")
])
@patch('builtins.input')
def test_menu(mock_input, input_value, expected_choice):
    """Test the menu function for correct user input handling."""
    mock_input.side_effect = [input_value]
    choice = UserInterface.menu()
    assert choice == expected_choice


# Test the get_user_preference function for correct input handling
@pytest.mark.parametrize("input_values, expected_preference", [
    (["1"], 'time'),
    (["2"], 'cost'),
    (["3"], 'transfers'),
    (["invalid", "2"], 'cost')  # Invalid input followed by valid input
])
@patch('builtins.input')
def test_get_user_preference(mock_input, input_values, expected_preference):
    """Test the get_user_preference function for correct input handling."""
    mock_input.side_effect = input_values
    preference = UserInterface.get_user_preference()
    assert preference == expected_preference


# Test the print_route_information function for correct output
@patch('builtins.print')
def test_print_route_information(mock_print):
    """Test the print_route_information function for correct output."""
    # Sample data for the test
    route = ["tarjan_home", "Relative_1", "Relative_2"]
    distance = 10.5
    preference = "time"
    route_modes = [("tarjan_home", "Relative_1", "bus"), ("Relative_1", "Relative_2", "train")]
    total_distance = 20.5  # Add a value for total_distance

    # Call the method to print route information
    UserInterface.print_route_information(route, distance, preference, route_modes, total_distance)

    # Check that the correct information is printed
    mock_print.assert_any_call(f"Optimal route based {preference}:")
    mock_print.assert_any_call(f"Route: {route}")
    mock_print.assert_any_call(f"Total Distance: {total_distance:.2f} km")
    if preference == "time": 
        mock_print.assert_any_call(f"time spent traveling: {60*distance:.2f} minutes")
    if preference == "cost": 
        mock_print.assert_any_call(f"cost for the journey:  {distance:.2f}")
    if preference == "transfers": 
        mock_print.assert_any_call(f"Time spent on transfers: {60*distance:.2f} minutes")
            
    mock_print.assert_any_call("\nTransport Modes:")
    mock_print.assert_any_call("tarjan_home -> Relative_1: bus")
    mock_print.assert_any_call("Relative_1 -> Relative_2: train")
