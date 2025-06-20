from search_algorithms import (
    romania_map,
    greedy_best_first_search,
    a_star_search,
    hill_climbing,
    simulated_annealing
)

def print_all_cities():
    print("Here are all the possible Romania cities that can be traveled:")
    print(sorted(romania_map.keys()))

def validate_city(city):
    return city in romania_map

def prompt_for_city(prompt_message):
    while True:
        city = input(prompt_message).strip()
        if validate_city(city):
            return city
        else:
            print(f"Could not find {city}, please try again.")

def get_valid_city_pair():
    while True:
        origin = prompt_for_city("Please enter the origin city: ")
        destination = prompt_for_city("Please enter the destination city: ")
        if origin == destination:
            print("The same city can't be both origin and destination. Please try again.")
        else:
            return origin, destination

def print_result(method_name, path):
    print(f"{method_name}")
    if path:
        total_cost = sum(romania_map[path[i]][path[i+1]] for i in range(len(path)-1))
        print(" → ".join(path))
        print(f"Total Cost: {total_cost}")
    else:
        print("No valid path found.")

def main():
    print_all_cities()
    while True:
        origin, destination = get_valid_city_pair()
        print_result("Greedy Best-First Search", greedy_best_first_search(origin, destination))
        print_result("A* Search", a_star_search(origin, destination))
        print_result("Hill Climbing Search", hill_climbing(origin, destination))
        print_result("Simulated Annealing Search", simulated_annealing(origin, destination))
        again = input("Would you like to find the best path between the other two cities? (yes/no): ").strip().lower()
        if again != 'yes':
            print("Thank You for Using Our App")
            break

if __name__ == "__main__":
    main()
