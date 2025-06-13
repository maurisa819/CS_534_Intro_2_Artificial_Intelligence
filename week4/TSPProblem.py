from search import *
import numpy as np

distances = {}
all_cities = []

class TSP_problem(Problem):

    """ subclass of Problem to define various functions """

    def two_opt(self, state):
        """ Neighbour generating function for Traveling Salesman Problem """
        neighbour_state = state[:]
        left = random.randint(0, len(neighbour_state) - 1)
        right = random.randint(0, len(neighbour_state) - 1)
        if left > right:
            left, right = right, left
        neighbour_state[left: right + 1] = reversed(neighbour_state[left: right + 1])
        return neighbour_state

    def actions(self, state):
        """ action that can be excuted in given state """
        return [self.two_opt]

    def result(self, state, action):
        """  result after applying the given action on the given state """
        return action(state)

    def path_cost(self, c, state1, action, state2):
        """ total distance for the Traveling Salesman to be covered if in state2  """
        cost = 0
        for i in range(len(state2) - 1):
            cost += distances[state2[i]][state2[i + 1]]
        cost += distances[state2[0]][state2[-1]]
        return cost

    def value(self, state):
        """ value of path cost given negative for the given state """
        return -1 * self.path_cost(None, None, None, state)

def hill_climbing(problem):
    """From the initial node, keep choosing the neighbor with highest value,
    stopping when no neighbor is better. [Figure 4.2]"""

    def find_neighbors(state, number_of_neighbors=100):
        """ finds neighbors using two_opt method """

        neighbors = []

        for i in range(number_of_neighbors):
            new_state = problem.two_opt(state)
            neighbors.append(Node(new_state))
            state = new_state

        return neighbors

    # as this is a stochastic algorithm, we will set a cap on the number of iterations
    iterations = 10000

    current = Node(problem.initial)

    while iterations:
        neighbors = find_neighbors(current.state)
        if not neighbors:
            break
        neighbor = argmax_random_tie(neighbors,
                                     key=lambda node: problem.value(node.state))
        if problem.value(neighbor.state) > problem.value(current.state):
            current.state = neighbor.state
        iterations -= 1

    return current.state

def main():
    for city in romania_map.locations.keys():
        distances[city] = {}
        all_cities.append(city)

    all_cities.sort()
    print("All the sorted cities in Romania:")
    print(all_cities)
    print()

    for name_1, coordinates_1 in romania_map.locations.items():
            for name_2, coordinates_2 in romania_map.locations.items():
                distances[name_1][name_2] = np.linalg.norm(
                    [coordinates_1[0] - coordinates_2[0], coordinates_1[1] - coordinates_2[1]])
                distances[name_2][name_1] = np.linalg.norm(
                    [coordinates_1[0] - coordinates_2[0], coordinates_1[1] - coordinates_2[1]])

    tsp = TSP_problem(all_cities)

    print("One shortest possible route that visits each city exactly once and returns to the origin city:")
    print(hill_climbing(tsp))

if __name__ == "__main__":
    main()