from tarjan_planner.route_bruteforce import RoutePlanner
class UserInterface:

    @staticmethod
    def menu(): 
        print("Choose a option:")
        print("1. Calculate a route based on preference")
        print("2. Choose starting location ")
        print("3. Add a new location to the planner ")
        print("4. Remove a location ")
        print("5. Show saved routes")
        print("6. Export the route")
        print("7. Exit\n")
        userInput = input()
        return userInput


       


    @staticmethod
    def get_user_preference():
        """
        Function to prompt the user for their choice of preference for the route planner.
        Valid options: 'time', 'cost', or 'transfers'.
        """
        print("Please choose your preference for route optimization:")
        print("1. Time")
        print("2. Cost")
        print("3. Transfers")

        while True:
            try: 
                user_input = input("Enter 1, 2, or 3: ").strip()

                if user_input == '1':
                    return 'time'
                elif user_input == '2':
                    return 'cost'
                elif user_input == '3':
                    return 'transfers'
                else:
                    print("Invalid input. Please enter a valid option.")
            except ValueError: 
                print("Error: Please enter a valid number for the menu option.\n")
                continue


    @staticmethod
    def print_route_information(route, distance, preference, route_modes):
        print(f"Optimal route based on {preference}:")
        #print(f"Route: {route}")
        print(f"Distance: {distance:.2f} km")
        #print(f"Execution time: {execution_time:.2f} seconds")

        print("\nTransport Modes:")
        for start, end, mode in route_modes:
            print(f"{start} -> {end}: {mode}")
