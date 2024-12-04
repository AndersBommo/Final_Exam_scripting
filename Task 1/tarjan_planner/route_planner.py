import networkx as nx
from tarjan_planner.distance_calculator import DistanceCalculator
import matplotlib.pyplot as plt
from tarjan_planner.time_logger import TimeLogger

class RoutePlanner:
    def __init__(self):
        # Initialize the graph, distance calculator, and relative data
        self.graph = nx.Graph()
        self.dist_calc = DistanceCalculator()
        self.relatives = self.load_relatives()
        self.transport_modes = self.get_transport_modes()
        self.build_graph()

    def load_relatives(self):
        # Load relatives with their coordinates (latitude, longitude)
        return {
            "tarjan_home": (37.5326, 126.9536), 
            "Relative_1": (37.4979, 127.0276),
            "Relative_2": (37.4833, 127.0322),
            "Relative_3": (37.5172, 127.0286),
            "Relative_4": (37.5219, 127.0411),
            "Relative_5": (37.5340, 127.0026),
            "Relative_6": (37.5443, 127.0557),
            "Relative_7": (37.5172, 127.0391),
            "Relative_8": (37.5800, 126.9844),
            "Relative_9": (37.5110, 127.0590),
            "Relative_10": (37.5133, 127.1028),
        }

    def get_transport_modes(self):
        # Transport modes with speed, cost per km, and transfer time
        return {
            "bus": {"speed": 40, "cost_per_km": 2, "color": "blue", "transfer_time": 5/60},
            "train": {"speed": 80, "cost_per_km": 5, "color": "green","transfer_time": 2/60},
            "bicycle": {"speed": 15, "cost_per_km": 0, "color": "orange", "transfer_time": 1/60},
            "walking": {"speed": 5, "cost_per_km": 0, "color": "red","transfer_time": 0},
        }

    def select_transport_mode(self, distance, preference="time"):
       
        transport_modes = self.get_transport_modes()

        if distance < 1:
            return "walking"
        elif distance < 5:
            return "bicycle"

        if preference == "time":
            # Time preference, scaling transfer time by distance
            selected_mode = min(
                transport_modes,
                key=lambda mode: (distance / transport_modes[mode]["speed"]) + (transport_modes[mode]["transfer_time"])
            )
        elif preference == "cost":
            # Cost preference, reducing cost weight for shorter distances
            selected_mode = min(
                transport_modes,
                key=lambda mode: (distance * transport_modes[mode]["cost_per_km"]) + (distance / transport_modes[mode]["speed"])
            )
        elif preference == "transfers":
            selected_mode = min(
                transport_modes,
                key=lambda mode: transport_modes[mode]["transfer_time"]
            )
        else:
            # Default to bus or train for larger distances
            if distance < 15:
                selected_mode = "bus"
            else:
                selected_mode = "train"

        return selected_mode



    def build_graph(self, preference="time"):
        self.graph.clear()
        relatives = list(self.relatives.keys())
        for i in range(len(relatives)):
            for j in range(i + 1, len(relatives)):
                loc1 = self.relatives[relatives[i]]
                loc2 = self.relatives[relatives[j]]
                distance = self.dist_calc.calculate_distance(loc1, loc2)

                transport_mode = self.select_transport_mode(distance, preference)
                time = distance / self.transport_modes[transport_mode]["speed"]
                cost = distance * self.transport_modes[transport_mode]["cost_per_km"]
                transfer_time = self.transport_modes[transport_mode]["transfer_time"]

                self.graph.add_edge(
                    relatives[i],
                    relatives[j],
                    distance=distance,
                    time=time,
                    cost=cost,
                    transfer_time=transfer_time,
                    mode=transport_mode
                )

    @TimeLogger.log_time
    def find_best_route_all_relatives(self, preference="time"):
        self.build_graph(preference)
        relatives = list(self.relatives.keys())
        
        # Create a list to store the route
        route = []
        current_location = "tarjan_home"  # Start at home
        visited = set([current_location])  # Keep track of visited relatives

        # Visit each relative using Dijkstra for the shortest time, cost, or transfers
        while len(route) < len(relatives) - 1:
            # Find the nearest relative based on the selected preference
            best_next_relative = None
            best_distance = float("inf")
            
            for relative in relatives:
                if relative not in visited:
                    if preference == "time":
                        next_relative = self.optimize_for_time(current_location, relative)
                    elif preference == "cost":
                        next_relative = self.optimize_for_cost(current_location, relative)
                    else:
                        next_relative = self.optimize_for_transfers(current_location, relative)
                    
                    # Calculate the "best" relative (with the shortest distance/time/cost)
                    distance = nx.shortest_path_length(self.graph, current_location, relative, weight=preference)
                    if distance < best_distance:
                        best_distance = distance
                        best_next_relative = relative
            
            # Update the current location and mark it as visited
            route.append(best_next_relative)
            visited.add(best_next_relative)
            current_location = best_next_relative

        return route

        """
            self.build_graph(preference)
            #self.print_distances()
            #print("called distances")
            weight_map = {"time": "time", "cost": "cost", "transfers": "transfer_time"}
            weight = weight_map.get(preference, "distance")
            tsp_path = nx.approximation.traveling_salesman_problem(self.graph, cycle=True, weight=weight)
            
            print("Distances for the best route:")
            for i in range(len(tsp_path) - 1):
                start = tsp_path[i]
                end = tsp_path[i + 1]
                distance = self.graph[start][end]["distance"]
                mode = self.graph[start][end]["mode"]

                print(f"Distance between {start} and {end}: {distance:.2f} km, Transport Mode: {mode}")
            
            return tsp_path"""


    def plot_route(self, route):
        plt.figure(figsize=(8, 6))

        legend_modes = set()

        for i in range(len(route) - 1):
            start, end = route[i], route[i + 1]
            lat_start, lon_start = self.relatives[start]
            lat_end, lon_end = self.relatives[end]

            # Fetch the edge attributes
            edge_data = self.graph[start][end]
            mode = edge_data.get("mode", "unknown")
            color = self.transport_modes[mode]["color"]

            if mode not in legend_modes:
                plt.plot([lon_start, lon_end], [lat_start, lat_end], color=color, label=mode)
                legend_modes.add(mode)
            else:
                plt.plot([lon_start, lon_end], [lat_start, lat_end], color=color)


            plt.plot(lon_start, lat_start, 'o', color=color)
            plt.text(lon_start, lat_start, start, fontsize=9, ha='right')

            plt.arrow(
            lon_start, lat_start,  # Start coordinates
            lon_end - lon_start, lat_end - lat_start,  # Arrow vector
            color=color,
                head_width=0.004, head_length=0.002, # Adjust head size
            length_includes_head=True
            )

        final_lat, final_lon = self.relatives[route[-1]]
        plt.plot(final_lon, final_lat, 'o', color="black")
        plt.text(final_lon, final_lat, route[-1], fontsize=8, ha='right')

        plt.xlabel("Longitude")
        plt.ylabel("Latitude")
        plt.title("Optimal Route with Transport Modes")
        plt.legend(loc="upper left")
        plt.grid(True)
        plt.show()

    def find_best_route(self, preference="time"):
        # Implement shortest path based on time, cost, or transfers
        start = "tarjan_home"
        target = "Relative_10"
        if preference == "time":
            return self.optimize_for_time(start, target)
        elif preference == "cost":
            return self.optimize_for_cost(start, target)
        else:
            return self.optimize_for_transfers(start, target)

    def optimize_for_time(self, start, target):
        # Dijkstra's algorithm for shortest time
        return nx.dijkstra_path(self.graph, start, target, weight="time")

    def optimize_for_cost(self, start, target):
        # Dijkstra's algorithm for least cost
        return nx.dijkstra_path(self.graph, start, target, weight="cost")

    def optimize_for_transfers(self, start, target):
    # Simplified implementation using edge attribute `transfer_time`
        return nx.shortest_path(self.graph, start, target, weight="transfer_time")
    def print_distances(self):
        # Iterate through the edges of the graph and print distances
        for start, end, data in self.graph.edges(data=True):
            distance = data.get("distance")
            print(f"Distance between {start} and {end}: {distance:.2f} km")

    def calculate_total_distance(self, route):
        """
        Calculate the total distance traveled based on the route.
        :param route: List of locations in the order they are visited.
        :return: Total distance traveled.
        """
        total_distance = 0
        for i in range(len(route) - 1):
            # Get the distance between two consecutive locations
            start, end = route[i], route[i + 1]
            total_distance += self.get_distance_between(start, end)
        
        print(f"Total Distance Traveled: {total_distance:.2f} km")
        return total_distance


    def calculate_total_time(self, route, selected_modes):
        """
        Calculate the total time taken for the journey.
        :param route: List of locations in the order they are visited.
        :param selected_modes: List of transport modes used for each segment of the journey.
        :return: Total time taken for the journey.
        """
        transport_modes = self.get_transport_modes()
        total_time = 0
        for i in range(len(route) - 1):
            start, end = route[i], route[i + 1]
            mode = selected_modes[i]  # Mode selected for this segment
            distance = self.get_distance_between(start, end)
            speed = transport_modes[mode]["speed"]
            transfer_time = transport_modes[mode]["transfer_time"]
            
            # Calculate travel time for this segment
            travel_time = (distance / speed) + transfer_time
            total_time += travel_time

        print(f"Total Time Taken: {total_time:.2f} hours")
        return total_time

    def print_information(self): 
        self.print_distances()
        self.calculate_total_distance()
        self.calculate_total_time
        



