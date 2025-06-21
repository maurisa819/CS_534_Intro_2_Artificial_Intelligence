"""
SimpleProblemSolvingAgent module implementing multiple search algorithms
for finding shortest or heuristic paths on the Romania road map.
"""

import math
import random
from queue import PriorityQueue

# -----------------------------------------------------------------------------
# DATA DEFINITIONS
# ROMANIA_ROAD_MAP and CITY_COORDINATES are referred at GitHub Source Code (AIMA-Python)
# aimacode. (2024). aima-python: Python implementation of algorithms from Artificial
# Intelligence: A Modern Approach (4th ed.) [Source code]. GitHub. https://github.com/aimacode/aima-python
# -----------------------------------------------------------------------------

# Road distances between Romanian cities (undirected graph).
# Each key maps to neighbors and the driving distance (in km).
ROMANIA_ROAD_MAP = {
    "Arad": {"Zerind": 75, "Sibiu": 140, "Timisoara": 118},
    "Bucharest": {"Urziceni": 85, "Pitesti": 101, "Giurgiu": 90, "Fagaras": 211},
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

# Straight-line (Euclidean) coordinates used for heuristic estimates.
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
    Agent that encapsulates four search strategies on the Romania map:
      1. Greedy Best-First Search
      2. A* Search
      3. Hill Climbing
      4. Simulated Annealing
    """

    def __init__(self):
        """
        Initialize the graph structure and heuristic locations.
        """
        self.graph = ROMANIA_ROAD_MAP  # road network
        self.locations = CITY_COORDINATES  # for heuristic computation

    def heuristic(self, node: str, goal: str) -> float:
        """
        Straight-line (Euclidean) distance between 'node' and 'goal'.

        Args:
            node: current city name.
            goal: target city name.

        Returns:
            Euclidean distance used as heuristic estimate.
        """
        x1, y1 = self.locations[node]
        x2, y2 = self.locations[goal]
        return math.hypot(x2 - x1, y2 - y1)

    def greedy_best_first_search(self, start: str, goal: str):
        """
        Perform Greedy Best-First Search: expand the node with
        lowest heuristic value first (no path-cost consideration).

        Returns:
            (path_list, total_cost)
        """
        frontier = PriorityQueue()
        # Priority = heuristic estimate; store (priority, path_so_far)
        frontier.put((self.heuristic(start, goal), [start]))
        explored = set()

        while not frontier.empty():
            _, path = frontier.get()
            node = path[-1]
            # Goal test
            if node == goal:
                return path, self.calculate_path_cost(path)
            if node in explored:
                continue
            explored.add(node)

            # Expand neighbors, prioritizing by heuristic only
            for neighbor in self.graph[node]:
                if neighbor not in explored:
                    new_path = path + [neighbor]
                    h_val = self.heuristic(neighbor, goal)
                    frontier.put((h_val, new_path))

        return [], float("inf")  # No path found

    def astar_search(self, start: str, goal: str):
        """
        Perform A* Search: combine path cost so far and heuristic.

        Returns:
            (path_list, total_cost)
        """
        frontier = PriorityQueue()
        # Priority = g + h; queue items: (priority, g_cost, path)
        frontier.put((self.heuristic(start, goal), 0, [start]))
        explored_costs = {}

        while not frontier.empty():
            f, cost_so_far, path = frontier.get()
            node = path[-1]
            # Goal test
            if node == goal:
                return path, cost_so_far

            # Skip if we have a cheaper path already
            if node in explored_costs and explored_costs[node] <= cost_so_far:
                continue
            explored_costs[node] = cost_so_far

            # Expand with path-cost + heuristic
            for neighbor, step_cost in self.graph[node].items():
                new_cost = cost_so_far + step_cost
                priority = new_cost + self.heuristic(neighbor, goal)
                frontier.put((priority, new_cost, path + [neighbor]))

        return [], float("inf")  # No path found

    def hill_climbing(self, start: str, goal: str):
        """
        Hill Climbing: always move to the neighbor with the
        best (lowest) heuristic, stopping at local maxima/minima.

        Returns:
            (path_list, total_cost)
        """
        path = [start]
        while True:
            node = path[-1]
            # Evaluate neighbors not yet visited
            candidates = [
                (nbr, self.heuristic(nbr, goal))
                for nbr in self.graph[node]
                if nbr not in path
            ]
            if not candidates:
                break
            # Pick neighbor with smallest heuristic
            best_nbr, best_h = min(candidates, key=lambda x: x[1])
            # Stop if no improvement
            if best_h >= self.heuristic(node, goal):
                break
            path.append(best_nbr)

        return path, self.calculate_path_cost(path)

    def simulated_annealing(
        self,
        start: str,
        goal: str,
        schedule=lambda t: 1.0 / (1 + t),
        max_steps: int = 1000,
        seed: int = 42,
    ):
        """
        Simulated Annealing: probabilistically accept worse moves early
        to escape local optima, cooling over time via 'schedule'.

        Args:
            start: origin city.
            goal: target city.
            schedule: temperature schedule function of step t.
            max_steps: maximum iterations allowed.
            seed: random seed for reproducibility.

        Returns:
            (path_list, total_cost)
        """
        random.seed(seed)
        path = [start]
        cost = self.calculate_path_cost(path)

        for t in range(max_steps):
            T = schedule(t)
            if T <= 0:
                break

            node = path[-1]
            # Possible next steps not in current path
            neighbors = [nbr for nbr in self.graph[node] if nbr not in path]
            if not neighbors:
                break

            next_node = random.choice(neighbors)
            next_path = path + [next_node]
            next_cost = self.calculate_path_cost(next_path)
            delta = next_cost - cost

            # Accept if better or by Boltzmann probability
            if delta < 0 or random.random() < math.exp(-delta / T):
                path, cost = next_path, next_cost

            if next_node == goal:
                break

        # If Annealing fails to reach goal, fallback to greedy best-first
        if not path or path[-1] != goal:
            return self.greedy_best_first_search(start, goal)

        return path, cost

    def calculate_path_cost(self, path: list) -> int:
        """
        Compute total driving distance of a given path.

        Args:
            path: ordered list of city names.

        Returns:
            Sum of edge distances along the path.
        """
        return sum(self.graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
