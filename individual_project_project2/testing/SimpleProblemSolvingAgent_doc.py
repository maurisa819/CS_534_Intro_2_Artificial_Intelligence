"""
SimpleProblemSolvingAgent module implementing multiple search algorithms
for finding shortest or heuristic paths on the Romania road map.
"""

import math  # for Euclidean distance and exp()
import random  # for simulated annealing randomness
from queue import PriorityQueue  # min-heap priority queue for best-first/A*

# -----------------------------------------------------------------------------
# DATA DEFINITIONS
# -----------------------------------------------------------------------------

# Road distances between Romanian cities (undirected graph).
ROMANIA_ROAD_MAP = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},  # neighbors of Arad
    "Bucharest": {
        "Urziceni": 85,
        "Pitesti": 101,
        "Giurgiu": 90,
        "Fagaras": 211,
    },  # neighbors of Bucharest
    "Craiova": {"Pitesti": 138, "Rimnicu": 146, "Drobeta": 120},
    "Drobeta": {"Mehadia": 75, "Craiova": 120},
    "Eforie": {"Hirsova": 86},
    "Fagaras": {"Sibiu": 99, "Bucharest": 211},
    "Giurgiu": {"Bucharest": 90},
    "Hirsova": {"Urziceni": 98, "Eforie": 86},
    "Iasi": {"Vaslui": 92, "Neamt": 87},
    "Lugoj": {"Timisoara": 111, "Mehadia": 70},
    "Mehadia": {"Lugoj": 70, "Drobeta": 75},
    "Neamt": {"Iasi": 87},
    "Oradea": {"Zerind": 71, "Sibiu": 151},
    "Pitesti": {"Rimnicu": 97, "Bucharest": 101, "Craiova": 138},
    "Rimnicu": {"Sibiu": 80, "Pitesti": 97, "Craiova": 146},
    "Sibiu": {"Arad": 140, "Oradea": 151, "Fagaras": 99, "Rimnicu": 80},
    "Timisoara": {"Arad": 118, "Lugoj": 111},
    "Urziceni": {"Bucharest": 85, "Hirsova": 98, "Vaslui": 142},
    "Vaslui": {"Iasi": 92, "Urziceni": 142},
    "Zerind": {"Arad": 75, "Oradea": 71},
}

# Straight-line coordinates for heuristic calculation.
CITY_COORDINATES = {
    "Arad": (91, 492),
    "Bucharest": (400, 327),
    "Craiova": (253, 288),
    "Drobeta": (165, 299),
    "Eforie": (562, 293),
    "Fagaras": (305, 449),
    "Giurgiu": (375, 270),
    "Hirsova": (534, 350),
    "Iasi": (473, 506),
    "Lugoj": (165, 379),
    "Mehadia": (168, 339),
    "Neamt": (406, 537),
    "Oradea": (131, 571),
    "Pitesti": (320, 368),
    "Rimnicu": (233, 410),
    "Sibiu": (207, 457),
    "Timisoara": (94, 410),
    "Urziceni": (456, 350),
    "Vaslui": (509, 444),
    "Zerind": (108, 531),
}


class SimpleProblemSolvingAgent:
    """
    Agent encapsulating four search strategies on the Romania map:
      1. Greedy Best-First Search
      2. A* Search
      3. Hill Climbing
      4. Simulated Annealing
    """

    def __init__(self):
        """
        Initialize agent with the road graph and city coordinates.
        """
        self.graph = ROMANIA_ROAD_MAP  # store the adjacency map
        self.locations = CITY_COORDINATES  # store heuristic coords

    def heuristic(self, node: str, goal: str) -> float:
        """
        Compute straight-line (Euclidean) distance between node and goal.
        """
        x1, y1 = self.locations[node]  # unpack coords of current node
        x2, y2 = self.locations[goal]  # unpack coords of goal
        return math.hypot(x2 - x1, y2 - y1)  # Euclidean formula

    def greedy_best_first_search(self, start: str, goal: str):
        """
        Greedy Best-First: expand node with smallest heuristic value.
        Returns: (path_list, total_cost)
        """
        frontier = PriorityQueue()  # min-heap ordered by heuristic
        frontier.put((self.heuristic(start, goal), [start]))  # seed with start
        explored = set()  # visited set

        while not frontier.empty():  # until no nodes left
            _, path = frontier.get()  # get path with best h-value
            node = path[-1]  # current city
            if node == goal:  # goal test
                return path, self.path_cost(path)
            if node in explored:  # skip if seen
                continue
            explored.add(node)  # mark explored

            # add all unseen neighbors to frontier
            for neighbor in self.graph[node]:
                if neighbor not in explored:
                    new_path = path + [neighbor]  # extend path
                    h = self.heuristic(neighbor, goal)  # compute h
                    frontier.put((h, new_path))  # push to PQ

        return [], float("inf")  # no path found

    def astar_search(self, start: str, goal: str):
        """
        A* Search: f(n)=g(n)+h(n). Returns shortest-cost path.
        """
        frontier = PriorityQueue()  # priority queue for f = g+h
        # initial item: (f, g, path)
        frontier.put((self.heuristic(start, goal), 0, [start]))
        explored_costs = {}  # best g-costs seen so far

        while not frontier.empty():
            f, cost_so_far, path = frontier.get()
            node = path[-1]  # current node
            if node == goal:  # goal reached
                return path, cost_so_far
            # if we've seen a cheaper path to node, skip
            if node in explored_costs and explored_costs[node] <= cost_so_far:
                continue
            explored_costs[node] = cost_so_far  # record best g-cost

            # expand neighbors
            for neighbor, step_cost in self.graph[node].items():
                new_cost = cost_so_far + step_cost  # g(n)
                priority = new_cost + self.heuristic(neighbor, goal)  # f(n)
                frontier.put((priority, new_cost, path + [neighbor]))

        return [], float("inf")  # no path found

    def hill_climbing(self, start: str, goal: str):
        """
        Hill Climbing: always move to neighbor with best (lowest) heuristic.
        Stops when no neighbor improves heuristic.
        """
        path = [start]  # initialize path
        while True:
            node = path[-1]  # current end of path
            # list of (neighbor, h-value) excluding visited
            candidates = [
                (nbr, self.heuristic(nbr, goal))
                for nbr in self.graph[node]
                if nbr not in path
            ]
            if not candidates:  # no moves available
                break
            best_nbr, best_h = min(candidates, key=lambda x: x[1])  # pick best
            # if best neighbor isn't better than current, stop
            if best_h >= self.heuristic(node, goal):
                break
            path.append(best_nbr)  # move to best neighbor

        return path, self.path_cost(path)

    def simulated_annealing(
        self,
        start: str,
        goal: str,
        schedule=lambda t: 1.0 / (1 + t),
        max_steps: int = 1000,
        seed: int = 42,
    ):
        """
        Simulated Annealing: probabilistically accept worse moves early.
        schedule(t) defines temperature T at step t.
        """
        random.seed(seed)  # ensure reproducibility
        path = [start]  # current path
        cost = self.path_cost(path)  # cost of current path

        for t in range(max_steps):  # iterate up to max_steps
            T = schedule(t)  # current temperature
            if T <= 0:
                break  # stop if cooled down fully

            node = path[-1]  # current city
            # possible next steps excluding visited
            neighbors = [nbr for nbr in self.graph[node] if nbr not in path]
            if not neighbors:
                break
            next_node = random.choice(neighbors)  # random neighbor choice
            next_path = path + [next_node]  # candidate path
            next_cost = self.path_cost(next_path)  # its cost
            delta = next_cost - cost  # cost difference

            # accept if better or with Boltzmann probability
            if delta < 0 or random.random() < math.exp(-delta / T):
                path, cost = next_path, next_cost  # update path & cost

            if next_node == goal:
                break  # stop if goal reached

        return path, cost  # final path & cost

    def path_cost(self, path: list) -> int:
        """
        Compute total driving distance along 'path'.
        """
        return sum(
            self.graph[path[i]][path[i + 1]]  # distance from city i to i+1
            for i in range(len(path) - 1)
        )
