"""
SimpleProblemSolvingAgent module implementing multiple search algorithms
for finding shortest or heuristic paths on the Romania road map.
"""

import math
import random

# For the Greedy Best-First Search and A* Search, the PriorityQueue module gave a very efficient "box"
# to store by priority (auto-sorting), not by index. This module also offer a safe thread producer-consumer
# model to parallelize an extend this application.
from queue import PriorityQueue  #

# -----------------------------------------------------------------------------
# DATA DEFINITIONS
# ROMANIA_ROAD_MAP and CITY_COORDINATES are referred at GitHub Source Code (AIMA-Python)
# aimacode. (2024). aima-python: Python implementation of algorithms from Artificial
# Intelligence: A Modern Approach (4th ed.) [Source code]. GitHub. https://github.com/aimacode/aima-python
# -----------------------------------------------------------------------------

# Road distances between Romanian cities (undirected graph).
# Each key maps to neighbors and the driving distance (in km).
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

# Straight-line coordinates used for heuristic estimates.
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

    # The SimpleProblemSolvingAgent class's heuristic method calculates the straight-line
    # distance between two cities or points. The heuristic method is employed by the Greedy Best-First and A* searches.
    # It is commonly used in geographical pathfinding because it is easy to calculate and provides a better lower
    # bound of the actual distance path.
    def heuristic(self, node: str, goal: str) -> float:
        """
        Straight-line (Euclidean) distance between 'node' and 'goal'.

        Args:
            node: current city name.
            goal: target city name.

        Returns:
            Euclidean distance used as heuristic estimate.
        """
        x1, y1 = self.locations[node]  # Setting the coordinates for the current city
        x2, y2 = self.locations[goal]  # Setting the coordinates for the target city
        return math.hypot(x2 - x1, y2 - y1)  # Euclidean formula

    # Greedy Best-First Search begins at a node, and we use a PriorityQueue, keyed by heuristic
    # distance to the goal, as the priority queue, and tracks visited nodes. It repeatedly extends
    # the node with the smallest heuristic, enqueues unvisited neighbors with their heuristic values,
    # and stops when the goal is found or the queue becomes empty. Fast but ignores path cost.
    def greedy_best_first_search(self, start: str, goal: str):
        """
        Perform Greedy Best-First Search: expand the node with
        lowest heuristic value first (no path-cost consideration).

        Returns:
            (path_list, total_cost)
        """
        frontier = PriorityQueue()  # Small heap order by priority
        # Priority = heuristic estimate; store (priority, path_so_far)
        frontier.put((self.heuristic(start, goal), [start]))  # Setting start
        explored = set()  # Visited set

        while not frontier.empty():  # Until no nodes are left
            _, path = frontier.get()  # get path with best heuristics value
            node = path[-1]  # current city
            # Testing the Goal
            if node == goal:
                return path, self.calculate_path_cost(path)
            if node in explored:  # skip if already visited
                continue
            explored.add(node)  # mark it visited or explored

            # Add all unvisited neighbors to frontier
            for neighbor in self.graph[node]:
                if neighbor not in explored:
                    new_path = path + [neighbor]
                    h_val = self.heuristic(neighbor, goal)
                    frontier.put((h_val, new_path))

        return [], float("inf")  # No path found

    # The A* Search algorithm sets up a priority queue with the start node scored by
    # f = g + h (with g = 0, h = heuristic). It tracks the best g-scores, repeatedly
    # extends the lowest f-score node, skips revisited nodes at a higher cost,
    # and enqueues neighbors with updated f-scores. It stops when it finds the goal.
    def astar_search(self, start: str, goal: str):
        """
        Perform A* Search: combine path cost so far and heuristic.

        Returns:
            (path_list, total_cost)
            A* Search: f(n)=g(n)+h(n). Returns shortest-cost path.
        """
        # priority queue for f [total cheapest solution cost, estimated]= g [cost so far] + h [heuristic estimate]
        frontier = PriorityQueue()
        # Priority = g + h; queue items: (priority, g_cost, path)
        frontier.put((self.heuristic(start, goal), 0, [start]))
        explored_costs = {}  # place holder for best g-costs seen so far

        while not frontier.empty():
            f, cost_so_far, path = frontier.get()
            node = path[-1]  # current node
            # Testing the Goal
            if node == goal:  # Goal found
                return path, cost_so_far

            # Skip if we have seen a cheaper path already
            if node in explored_costs and explored_costs[node] <= cost_so_far:
                continue
            explored_costs[node] = cost_so_far

            # Extend with path-cost + heuristic
            for neighbor, step_cost in self.graph[node].items():
                new_cost = cost_so_far + step_cost
                priority = new_cost + self.heuristic(neighbor, goal)
                frontier.put((priority, new_cost, path + [neighbor]))

        return [], float("inf")  # No path found

    # Hill Climbing starts at the initial node and repeatedly moves to the unvisited neighbor that has the
    # lowest heuristic distance to the goal. The process continues until no neighbor shows any improvement,
    # at which point it returns the path found. Although this method is straightforward, deterministic, and greedy,
    # it is susceptible to getting stuck in local optima, as it ignores the overall path cost.
    def hill_climbing(self, start: str, goal: str):
        """
        Hill Climbing: always move to the neighbor with the
        best (lowest) heuristic, stopping when no neighbor improves heuristic.

        Returns:
            (path_list, total_cost)
        """
        path = [start]  # initialize path
        while True:
            node = path[-1]  # current end of path
            #  list of (neighbor, h-value) excluding visited
            candidates = [
                (nbr, self.heuristic(nbr, goal))
                for nbr in self.graph[node]
                if nbr not in path
            ]
            if not candidates:  # no moves available
                break
            # Pick neighbor with smallest heuristic
            best_nbr, best_h = min(candidates, key=lambda x: x[1])
            # Stop if no improvement
            if best_h >= self.heuristic(node, goal):
                break
            path.append(best_nbr)  # move to best neighbor

        return path, self.calculate_path_cost(path)

    # In Simulated Annealing, whenever a proposed move increases the cost by a delta, it is not accepted.
    # Instead, it takes it with a probability that mirrors how, in a heated metal, higher‐energy states
    # are occupied with exactly this likelihood in statistical physics. This probability is known as
    # the Boltzmann probability.
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
        """
        random.seed(seed)
        path = [start]
        cost = self.calculate_path_cost(path)

        for t in range(max_steps):
            T = schedule(t)
            if T <= 0:
                break

            node = path[-1]
            neighbors = [nbr for nbr in self.graph[node] if nbr not in path]
            if not neighbors:
                break

            next_node = random.choice(neighbors)
            next_path = path + [next_node]
            next_cost = self.calculate_path_cost(next_path)
            delta = next_cost - cost

            # Accept better moves, or worse ones with Boltzmann probability
            if delta < 0 or random.random() < math.exp(-delta / T):
                path, cost = next_path, next_cost

            if path[-1] == goal:
                break

        # Fallback if we never reached the goal
        if path[-1] != goal:
            return self.greedy_best_first_search(start, goal)

        return path, cost

    # This method computes a path’s total distance by summing the edge weights or values of each pair.
    # It loops through indices 0…len(path)-2, looks up graph[path[i]][path[i+1]] for each consecutive city pair,
    # and uses sum() to aggregate those distances. The search algorithms use this cost to compare and rank paths.
    def calculate_path_cost(self, path: list) -> int:
        """
        Compute total driving distance of a given path.

        Args:
            path: ordered list of city names.

        Returns:
            Sum of edge distances along the path.
        """
        return sum(self.graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
