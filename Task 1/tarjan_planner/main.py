#main.py
from tarjan_planner.route_bruteforce import RoutePlanner
from tarjan_planner.interface import UserInterface

def main():
    planner = RoutePlanner()
    interface = UserInterface()

    print("Welcome to the Tarjan route planner\n")

    while True:
        try:
            # Wrap user input in a try block to handle invalid inputs
            userOption = int(interface.menu())
        except ValueError:
            print("Error: Please enter a valid number for the menu option.\n")
            continue  # Skip the rest of the loop and prompt again

        if userOption == 1: 
            try:
                preference = interface.get_user_preference()
                planner.build_graph(preference)  # Build the graph based on the preference
                print("Please wait for route calculation")

                # Unpack the result with execution time
                best_route, best_distance, route_modes = planner.find_best_route_all_relatives(preference)
                interface.print_route_information(best_route, best_distance, preference, route_modes)

                print("Do you wish to save this route?\n")
                save = input("yes or no\n").strip().lower()
                if save == "yes":
                    route_name = input("What do you wish to name this route? \n")
                    planner.save_route(route_name, best_route, best_distance, route_modes)
            except Exception as e:
                print(f"Error occurred while processing option 1: {e}\n")

        elif userOption == 2: 
            try:
                print("Available locations:", ", ".join(planner.relatives.keys()))
                new_start = input("Enter the name of the new starting point: ")
                planner.set_starting_point(new_start)
            except KeyError:
                print("Error: The starting point entered is not valid.\n")

        elif userOption == 3: 
            try:
                name = input("Enter the name of the new location: ")
                latitude = float(input("Enter the latitude of the location: "))
                longitude = float(input("Enter the longitude of the location: "))
                planner.add_location(name, latitude, longitude)
                print(f"Location {name} added successfully.\n")
            except ValueError:
                print("Error: Latitude and longitude must be numbers.\n")

        elif userOption == 4: 
            try:
                print("Available locations:", ", ".join(planner.relatives.keys()))
                location_to_remove = input("Enter the name of the location to remove: ").strip()
                planner.remove_location(location_to_remove)
            except KeyError:
                print(f"Error: The location '{location_to_remove}' does not exist.\n")

        elif userOption == 5: 
            planner.show_saved_routes()

        elif userOption == 6: 
            planner.export_route()

        elif userOption == 7: 
            break

        else: 
            print("Error: That is not a valid option.\n")

    print("Thanks for using Tarjan planner! Goodbye |=8-)")
        
if __name__ == "__main__":
    main()
