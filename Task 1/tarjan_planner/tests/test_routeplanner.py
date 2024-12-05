import pytest
from tarjan_planner.route_bruteforce import RoutePlanner


@pytest.fixture
def route_planner():
    """Fixture to create a RoutePlanner instance."""
    return RoutePlanner()


def test_load_relatives(route_planner):
    """Test if relatives are loaded correctly."""
    relatives = route_planner.relatives
    assert "tarjan_home" in relatives
    assert len(relatives) == 11  # Verify the number of loaded relatives


def test_add_location(route_planner):
    """Test adding a new location."""
    route_planner.add_location("New_Relative", 37.501, 127.002)
    assert "New_Relative" in route_planner.relatives
    assert route_planner.relatives["New_Relative"] == (37.501, 127.002)


def test_remove_location(route_planner):
    """Test removing an existing location."""
    route_planner.add_location("Temp_Relative", 37.501, 127.002)
    route_planner.remove_location("Temp_Relative")
    assert "Temp_Relative" not in route_planner.relatives


def test_set_starting_point(route_planner):
    """Test setting a valid starting point."""
    route_planner.set_starting_point("Relative_1")
    assert route_planner.starting_point == "Relative_1"


def test_build_graph(route_planner):
    """Test building the graph with the correct attributes."""
    preference = "time"
    route_planner.build_graph(preference)
    assert len(route_planner.graph.nodes) > 0
    assert len(route_planner.graph.edges) > 0

    # Verify that the graph has correct attributes
    for _, _, data in route_planner.graph.edges(data=True):
        assert "distance" in data
        assert "time" in data
        assert "cost" in data
        assert "transfer_time" in data
        assert "mode" in data


def test_brute_force_tsp(route_planner):
    """Test finding the best route using TSP."""
    preference = "time"
    route_planner.build_graph(preference)
    best_route, best_metric = route_planner.brute_force_tsp(preference)
    assert isinstance(best_route, list)
    assert len(best_route) > 0
    assert isinstance(best_metric, (float, int))


def test_save_route(route_planner):
    """Test saving a route."""
    preference = "time"
    route_planner.build_graph(preference)
    route = ["tarjan_home", "Relative_1", "Relative_2", "tarjan_home"]
    distance = 10.0
    transport_modes = [("tarjan_home", "Relative_1", "bus"), ("Relative_1", "Relative_2", "train")]

    route_planner.save_route("Test_Route", route, distance, transport_modes)
    assert "Test_Route" in route_planner.saved_routes
    saved_route = route_planner.saved_routes["Test_Route"]
    assert saved_route["route"] == route
    assert saved_route["distance"] == distance
    assert saved_route["transport_modes"] == transport_modes


def test_show_saved_routes(route_planner, capsys):
    """Test showing saved routes."""
    # Build the graph to ensure edges exist
    preference = "time"
    route_planner.build_graph(preference)

    # Define a sample route and save it
    route = ["tarjan_home", "Relative_1", "Relative_2", "tarjan_home"]
    distance = 10.0
    transport_modes = [("tarjan_home", "Relative_1", "bus"), ("Relative_1", "Relative_2", "train")]

    route_planner.save_route("Test_Route", route, distance, transport_modes)

    # Now show the saved routes
    route_planner.show_saved_routes()

    # Capture and verify printed output
    captured = capsys.readouterr()
    assert "Route Name: Test_Route" in captured.out
    assert "Total Distance: 10.00 km" in captured.out



def test_select_transport_mode(route_planner):
    """Test transport mode selection."""
    distance = 3.0
    mode = route_planner.select_transport_mode(distance, "time")
    assert mode in ["bus", "train", "bicycle", "walking"]


def test_plot_route(route_planner, tmp_path):
    """Test route plotting functionality."""
    route = ["tarjan_home", "Relative_1", "Relative_2", "tarjan_home"]
    preference = "time"
    route_planner.build_graph(preference)
    file_path = tmp_path / "test_plot.png"
    route_planner.plot_route(route, preference, show=False, save=str(file_path))
    assert file_path.exists()
