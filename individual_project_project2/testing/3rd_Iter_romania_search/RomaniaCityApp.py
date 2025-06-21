from SimpleProblemSolvingAgent import SimpleProblemSolvingAgent


def main():
    """
    Interactive CLI for finding paths between Romanian cities using
    multiple search algorithms.
    """
    agent = SimpleProblemSolvingAgent()
    cities = sorted(agent.graph.keys())
    print("Here are all the possible Romania cities that can be traveled:")
    print(cities)

    while True:
        # Prompt for origin city until valid
        print("Please enter the origin city: ", end="")
        origin = input().strip()
        while origin not in agent.graph:
            print(f"Could not find {origin}, please try again: ", end="")
            origin = input().strip()

        # Prompt for destination city until valid and distinct
        print("Please enter the destination city: ", end="")
        dest = input().strip()
        while dest not in agent.graph or dest == origin:
            if dest not in agent.graph:
                print(f"Could not find {dest}, please try again: ", end="")
                dest = input().strip()
            else:
                print(
                    "The same city can't be both origin and destination. Please try again. Please enter the destination city: ",
                    end="",
                )
                dest = input().strip()

        # Execute and display all search methods
        for name, func in [
            ("Greedy Best-First Search", agent.greedy_best_first_search),
            ("A* Search", agent.astar_search),
            ("Hill Climbing Search", agent.hill_climbing),
            ("Simulated Annealing Search", agent.simulated_annealing),
        ]:
            path, cost = func(origin, dest)
            print(name)
            print(" → ".join(path))
            print(f"Total Cost: {cost}")

        # Ask to run again or exit
        print(
            "Would you like to find the best path between the other two cities? ",
            end="",
        )
        again = input().strip().lower()
        if again not in ("yes", "y"):
            print("Thank You for Using Our App")
            break


if __name__ == "__main__":
    main()
