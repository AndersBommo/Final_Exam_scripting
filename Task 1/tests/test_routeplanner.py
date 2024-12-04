import unittest
from tarjan_planner.route_bruteforce import RoutePlanner


class TestRoutePlanner(unittest.TestCase):
    def setUp(self):
        """Set up the RoutePlanner instance for testing."""
        self.route_planner = RoutePlanner()

    def test_load_relatives(self):
        """Test if relatives are loaded correctly."""
        relatives = self.route_planner.relatives
        self.assertIn("tarjan_home", relatives)
        self.assertEqual(len(relatives), 11)  # Verify the number of loaded relatives

    def test_add_location(self):
        """Test adding a new location."""
        self.route_planner.add_location("New_Relative", 37.501, 127.002)
        self.assertIn("New_Relative", self.route_planner.relatives)
        self.assertEqual(self.route_planner.relatives["New_Relative"], (37.501, 127.002))

    def test_remove_location(self):
        """Test removing an existing location."""
        self.route_planner.add_location("Temp_Relative", 37.501, 127.002)
        self.route_planner.remove_location("Temp_Relative")
        self.assertNotIn("Temp_Relative", self.route_planner.relatives)

    def test_set_starting_point(self):
        """Test setting a valid starting point."""
        self.route_planner.set_starting_point("Relative_1")
        self.assertEqual(self.route_planner.starting_point, "Relative_1")

    def test_build_graph(self):
        """Test building the graph with the correct attributes."""
        preference = "time"
        self.route_planner.build_graph(preference)
        self.assertGreater(len(self.route_planner.graph.nodes), 0)
        self.assertGreater(len(self.route_planner.graph.edges), 0)

        # Verify that the graph has correct attributes
        for edge in self.route_planner.graph.edges(data=True):
            self.assertIn("distance", edge[2])
            self.assertIn("time", edge[2])
            self.assertIn("cost", edge[2])
            self.assertIn("transfer_time", edge[2])
            self.assertIn("mode", edge[2])

    def test_brute_force_tsp(self):
        """Test finding the best route using TSP."""
        preference = "time"
        self.route_planner.build_graph(preference)
        best_route, best_metric = self.route_planner.brute_force_tsp(preference)
        self.assertIsInstance(best_route, list)
        self.assertGreater(len(best_route), 0)
        self.assertIsInstance(best_metric, (float, int))

    def test_save_route(self):
        """Test saving a route."""
        preference = "time"
        self.route_planner.build_graph(preference)
        route = ["tarjan_home", "Relative_1", "Relative_2", "tarjan_home"]
        distance = 10.0
        transport_modes = [("tarjan_home", "Relative_1", "bus"), ("Relative_1", "Relative_2", "train")]

        self.route_planner.save_route("Test_Route", route, distance, transport_modes)
        print(self.assertIn("Test_Route", self.route_planner.saved_routes))
        self.assertIn("Test_Route", self.route_planner.saved_routes)

    def test_show_saved_routes(self):
        """Test showing saved routes."""
        preference = "time"
        self.route_planner.build_graph(preference)
        route = ["tarjan_home", "Relative_1", "Relative_2", "tarjan_home"]
        distance = 10.0
        transport_modes = [("tarjan_home", "Relative_1", "bus"), ("Relative_1", "Relative_2", "train")]

        self.route_planner.save_route("Test_Route", route, distance, transport_modes)
        print("route saved",self.route_planner.save_route("Test_Route", route, distance, transport_modes) )
        self.route_planner.show_saved_routes()


    def test_select_transport_mode(self):
        """Test transport mode selection."""
        distance = 3.0
        mode = self.route_planner.select_transport_mode(distance, "time")
        self.assertIn(mode, ["bus", "train", "bicycle", "walking"])

    def test_plot_route(self):
        """Test route plotting functionality."""
        route = ["tarjan_home", "Relative_1", "Relative_2", "tarjan_home"]
        preference = "time"
        self.route_planner.build_graph(preference)
        self.route_planner.plot_route(route, preference, show=False, save="test_plot.png")


if __name__ == "__main__":
    unittest.main()
