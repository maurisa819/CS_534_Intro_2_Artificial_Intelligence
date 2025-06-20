from SimpleProblemSolvingAgent import SimpleProblemSolvingAgent

def main():
    cities = sorted(SimpleProblemSolvingAgent._roads.keys())
    print("Here are all the possible Romania cities that can be traveled:")
    print(cities)

    while True:
        origin = input("\nPlease enter the origin city: ").strip().title()
        while origin not in cities:
            origin = input(f"Could not find {origin}, please try again: ").strip().title()

        dest = input("Please enter the destination city: ").strip().title()
        while dest not in cities:
            dest = input(f"Could not find {dest}, please try again: ").strip().title()

        if dest == origin:
            print("The same city can't be both origin and destination. Please try again.")
            continue

        agent = SimpleProblemSolvingAgent(origin, dest)

        result = agent.run_greedy()
        print("\nGreedy Best-First Search")
        print(" → ".join(result.solution_path()))
        print(f"Total Cost: {result.path_cost}")

        result = agent.run_astar()
        print("\nA* Search")
        print(" → ".join(result.solution_path()))
        print(f"Total Cost: {result.path_cost}")

        result = agent.run_hill_climbing()
        print("\nHill Climbing Search")
        print(" → ".join(result.solution_path()))
        print(f"Total Cost: {result.path_cost}")

        result = agent.run_simulated_annealing()
        print("\nSimulated Annealing Search")
        print(" → ".join(result.solution_path()))
        print(f"Total Cost: {result.path_cost}")

        again = input("\nWould you like to find the best path between the other two cities? ").strip().lower()
        if not again.startswith('y'):
            print("Thank You for Using Our App")
            break

if __name__ == "__main__":
    main()
