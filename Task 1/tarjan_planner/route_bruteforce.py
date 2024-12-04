import itertools
import networkx as nx
from tarjan_planner.distance_calculator import DistanceCalculator
import matplotlib.pyplot as plt
from tarjan_planner.time_logger import TimeLogger
import json
import csv

class RoutePlanner:
    def __init__(self):
        # Initialize the graph, distance calculator, and relative data
        self.graph = nx.Graph()
        self.dist_calc = DistanceCalculator()
        self.relatives = self.load_relatives()
        self.transport_modes = self.get_transport_modes()
        self.starting_point = "tarjan_home"
        self.saved_routes = {}
        

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
            #"Relative_7": (37.5172, 127.0391),
            #"Relative_8": (37.5800, 126.9844),
            #"Relative_9": (37.5110, 127.0590),
            #"Relative_10": (37.5133, 127.1028),
            
        }
    
    def add_location(self, name, latitude, longitude):
        """Add a new location to the relatives dictionary."""
        if name in self.relatives:
            print(f"Location '{name}' already exists.")
        else:
            self.relatives[name] = (latitude, longitude)
            print(f"Added new location: {name} at ({latitude}, {longitude}).")

    def remove_location(self, location_name):
        if location_name in self.relatives:
            if location_name == self.starting_point:
                print(f"Error: '{location_name}' is currently the starting point. Change the starting point before removing it.")
            else:
                del self.relatives[location_name]
                print(f"Location '{location_name}' has been removed.")
        else:
            print(f"Error: '{location_name}' is not a valid location.")



    def get_transport_modes(self):
        # Transport modes with speed, cost per km, and transfer time
        return {
            "bus": {"speed": 40, "cost_per_km": 2, "color": "blue", "transfer_time": 5/60},
            "train": {"speed": 80, "cost_per_km": 5, "color": "green","transfer_time": 2/60},
            "bicycle": {"speed": 15, "cost_per_km": 0, "color": "orange", "transfer_time": 1/60},
            "walking": {"speed": 5, "cost_per_km": 0, "color": "red","transfer_time": 0},
        }

    def select_transport_mode(self, distance, preference):
        transport_modes = self.get_transport_modes()

        # Handle short distances
        if distance < 1:
            return "walking"
        elif distance < 4:
            return "bicycle"
        
        # For distances over 4km, choose between bus or train based on preference
        if preference == "time":
            # Choose the fastest between bus and train
            selected_mode = min(
                ["bus", "train"],
                key=lambda mode: (distance / transport_modes[mode]["speed"]) + transport_modes[mode]["transfer_time"]
            )
        elif preference == "cost":
            # Choose the cheapest between bus and train
            selected_mode = min(
                ["bus", "train"],
                key=lambda mode: (distance * transport_modes[mode]["cost_per_km"])
            )
        elif preference == "transfers":
            # Choose the mode with the least transfer time
            selected_mode = min(
                ["bus", "train"],
                key=lambda mode: transport_modes[mode]["transfer_time"]
            )
        else:
            # Default to train if no preference is provided
            selected_mode = "train"

        return selected_mode

    def set_starting_point(self, new_start):
        if new_start in self.relatives:
            self.starting_point = new_start
            print(f"Starting point updated to: {new_start}")
        else:
            print(f"Error: '{new_start}' is not a valid location.")

    def brute_force_tsp(self, preference):
        self.build_graph(preference)
        relatives = list(self.relatives.keys())
        route_counter = 0
        # Generate all possible permutations of the relatives (excluding the start node)
        
        start = self.starting_point
        relatives.remove(start)
        permutations = itertools.permutations(relatives)

        best_route = None
        best_metric = float('inf')

        # Iterate through all permutations to find the shortest route
        for perm in permutations:
            route = [start] + list(perm) + [start]
            total_metric = 0  # Start with zero time
            route_counter += 1


        # Calculate total time for the route considering transport modes
            for i in range(len(route) - 1):
                start_node = route[i]
                end_node = route[i + 1]
                edge_data = self.graph[start_node][end_node]
                distance = self.graph[start_node][end_node]["distance"]   # Assuming you have a method to calculate the distance
                mode = self.select_transport_mode(distance, preference)  # Get transport mode based on preference
                transport_modes = self.get_transport_modes()

                if preference == "time":
                    total_metric += edge_data["time"]
                elif preference == "cost":
                    total_metric += edge_data["cost"]
                elif preference == "transfers":
                    total_metric += edge_data["transfer_time"]
                else:
                    # Default to time if no preference is provided
                    total_metric += edge_data["time"]
            if total_metric < best_metric:
                best_metric = total_metric
                best_route = route

        print(best_metric, preference)

        return best_route, best_metric

    def build_graph(self, preference, mode=[]):
        self.graph.clear()
        relatives = list(self.relatives.keys())
        mode=[]
        for i in range(len(relatives)):
            for j in range(i + 1, len(relatives)):
                loc1 = self.relatives[relatives[i]]
                loc2 = self.relatives[relatives[j]]
                distance = self.dist_calc.calculate_distance(loc1, loc2)

                transport_mode = self.select_transport_mode(distance, preference)
                time = distance / self.transport_modes[transport_mode]["speed"]
                cost = distance * self.transport_modes[transport_mode]["cost_per_km"]
                transfer_time = self.transport_modes[transport_mode]["transfer_time"]
                mode.append(self.transport_modes)
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
    def find_best_route_all_relatives(self, preference):
        best_route, best_metric = self.brute_force_tsp(preference)
    
        # Extract transport modes for the route
        route_modes = [
            (start, end, self.graph[start][end]["mode"])
            for start, end in zip(best_route[:-1], best_route[1:])
        ]

        print(f"Shortest route: {best_route}")
        print(f"Total distance: {best_metric:.2f} km")
        return best_route, best_metric, route_modes

    
    def get_route_transport_modes(self, route):
        transport_modes = []
        for i in range(len(route) - 1):
            start, end = route[i], route[i + 1]
            mode = self.graph[start][end]["mode"]
            transport_modes.append((start, end, mode))
        return transport_modes

    #### SJEKK DENNE####
    def save_route(self, route_name, route, distance, transport_modes):
        if route_name in self.saved_routes:
            print(f"A route named '{route_name}' already exists. Overwriting it.")
        self.saved_routes[route_name] = {
            "route": route,
            "distance": distance,
            "transport_modes": transport_modes
        }
        print(f"Route '{route_name}' has been saved.")

    
    def show_saved_routes(self):
        if not self.saved_routes:
            print("No saved routes available.")
        else:
            print("Saved Routes:")
            for name, data in self.saved_routes.items():
                route = data["route"]
                print(f"  - Route Name: {name}")
                print("    Route details:")
                for i in range(len(route) - 1):
                    start = route[i]
                    end = route[i + 1]
                    # Retrieve transport mode between start and end
                    edge_data = self.graph[start][end]
                    mode = edge_data.get("mode", "unknown")  # Assume mode is stored in the graph
                    print(f"    {start} -> {end}: {mode}")
                print(f"    Total Distance: {data['distance']:.2f} km\n")



    def export_route(self):
        if not self.saved_routes:
            print("No saved routes available to export.")
            return

        print("Available Routes:")
        for route_name in self.saved_routes:
            print(f"  - {route_name}")

        # Loop until a valid route name is provided or the user chooses to return
        while True:
            selected_route = input("Enter the name of the route you want to export or type 'back' to return to the main menu: ").strip()
            if selected_route.lower() == 'back':
                print("Returning to the main menu.")
                return
            if selected_route in self.saved_routes:
                break
            print(f"Route '{selected_route}' does not exist. Please enter a valid route name.")

        # Retrieve route details
        route_data = self.saved_routes[selected_route]
        route = route_data["route"]
        distance = route_data["distance"]
        preference = route_data.get("preference", "unknown")

        # Loop until a valid export option is chosen or the user chooses to return
        while True:
            print("Choose export format:")
            print("1. CSV")
            print("2. JSON")
            print("3. Plot")
            print("4. Back to main menu")

            export_format = input("Enter your choice (1, 2, 3, or 4): ").strip()

            if export_format == "1":  # Export as CSV
                file_name = f"exported_routes/{selected_route}_route.csv"
                try:
                    with open(file_name, mode="w", newline="") as file:
                        writer = csv.writer(file)
                        writer.writerow(["Start", "End", "Transport Mode"])
                        for i in range(len(route) - 1):
                            start = route[i]
                            end = route[i + 1]
                            mode = self.graph[start][end].get("mode", "unknown")
                            writer.writerow([start, end, mode])
                        writer.writerow(["Total Distance", f"{distance:.2f} km"])
                    print(f"Route '{selected_route}' has been exported as {file_name}.\n")
                except Exception as e:
                    print(f"An error occurred while exporting the route as CSV: {e}")
                break

            elif export_format == "2":  # Export as JSON
                file_name = f"exported_routes/{selected_route}_route.json"
                try:
                    json_data = {
                        "route_name": selected_route,
                        "route": [
                            {
                                "start": route[i],
                                "end": route[i + 1],
                                "transport_mode": self.graph[route[i]][route[i + 1]].get("mode", "unknown")
                            }
                            for i in range(len(route) - 1)
                        ],
                        "total_distance": f"{distance:.2f} km"
                    }
                    with open(file_name, "w") as file:
                        json.dump(json_data, file, indent=4)
                    print(f"Route '{selected_route}' has been exported as {file_name}.\n")
                except Exception as e:
                    print(f"An error occurred while exporting the route as JSON: {e}")
                break

            elif export_format == "3":  # Export the plot
                try:
                    import os
                    os.makedirs("exported_routes", exist_ok=True)  # Create directory if it doesn't exist
                    file_name = f"exported_routes/{selected_route}_route_plot.png"
                    self.plot_route(route, preference, show=False, save=file_name)  # Save the plot without showing
                    print(f"Route '{selected_route}' plot has been saved as {file_name}.\n")
                except Exception as e:
                    print(f"An error occurred while exporting the route plot: {e}")
                break

            elif export_format == "4":  # Return to main menu
                print("Returning to the main menu.\n")
                return

            else:
                print("Invalid choice. Please enter 1, 2, 3, or 4.")






    def plot_route(self, route, preference, show=True, save = None):
        plt.figure(figsize=(8, 6))

        legend_modes = set()

        for i in range(len(route) - 1):
            start, end = route[i], route[i + 1]
            
            # Ensure start and end are strings and not lists or other types
            if isinstance(start, list) or isinstance(end, list):
                print(f"Error: Start or end is a list, but it should be a string. Start: {start}, End: {end}")
                continue  # Skip invalid entries

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
        plt.title(f"Optimal Route with Transport Modes based on {preference}")
        plt.legend(loc="upper left")
        plt.grid(True)
        if save:  # Save the plot if a file path is provided
            plt.savefig(save)
            print(f"Plot saved to {save}")
        if show:  # Show the plot if requested
            plt.show()

    def calculate_total_distance(self, route):
        total_distance = 0
        for i in range(len(route) - 1):
            start, end = route[i], route[i + 1]
            total_distance += self.graph[start][end]["distance"]

        return total_distance
