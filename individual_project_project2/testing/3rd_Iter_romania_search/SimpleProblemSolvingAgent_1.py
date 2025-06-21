"""
SimpleProblemSolvingAgent module implementing search algorithms for pathfinding on Romania map.
"""

import math
import random

# Romania road map distances (kilometers)
# GitHub Source Code (AIMA-Python)
# aimacode. (2024). aima-python: Python implementation of algorithms from Artificial Intelligence:
# A Modern Approach (4th ed.) [Source code]. GitHub. https://github.com/aimacode/aima-python

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

# Straight-line coordinates for heuristic
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
    def __init__(self):
        self.graph = ROMANIA_ROAD_MAP
        self.locations = CITY_COORDINATES

    def heuristic(self, node, goal):
        x1, y1 = self.locations[node]
        x2, y2 = self.locations[goal]
        return math.hypot(x2 - x1, y2 - y1)

    def greedy_best_first_search(self, start, goal):
        from queue import PriorityQueue

        frontier = PriorityQueue()
        frontier.put((self.heuristic(start, goal), [start]))
        explored = set()
        while not frontier.empty():
            _, path = frontier.get()
            node = path[-1]
            if node == goal:
                return path, self._path_cost(path)
            if node not in explored:
                explored.add(node)
                for neighbor in self.graph[node]:
                    if neighbor not in explored:
                        frontier.put(
                            (self.heuristic(neighbor, goal), path + [neighbor])
                        )
        return [], float("inf")

    def astar_search(self, start, goal):
        from queue import PriorityQueue

        frontier = PriorityQueue()
        frontier.put((self.heuristic(start, goal), 0, [start]))
        explored = {}
        while not frontier.empty():
            f, cost_so_far, path = frontier.get()
            node = path[-1]
            if node == goal:
                return path, cost_so_far
            if node in explored and explored[node] <= cost_so_far:
                continue
            explored[node] = cost_so_far
            for neighbor, cost in self.graph[node].items():
                new_cost = cost_so_far + cost
                frontier.put(
                    (
                        new_cost + self.heuristic(neighbor, goal),
                        new_cost,
                        path + [neighbor],
                    )
                )
        return [], float("inf")

    def hill_climbing(self, start, goal):
        current = [start]
        while True:
            node = current[-1]
            neighbors = [
                (n, self.heuristic(n, goal))
                for n in self.graph[node]
                if n not in current
            ]
            if not neighbors:
                break
            best_neighbor, best_h = min(neighbors, key=lambda x: x[1])
            if best_h >= self.heuristic(node, goal):
                break
            current.append(best_neighbor)
        return current, self._path_cost(current)

    def simulated_annealing(
        self, start, goal, schedule=lambda t: 1.0 / (1 + t), max_steps=1000, seed=42
    ):
        random.seed(seed)
        current = [start]
        current_cost = self._path_cost(current)
        for t in range(max_steps):
            T = schedule(t)
            if T <= 0:
                break
            node = current[-1]
            neighbors = [n for n in self.graph[node] if n not in current]
            if not neighbors:
                break
            next_node = random.choice(neighbors)
            next_path = current + [next_node]
            next_cost = self._path_cost(next_path)
            delta = next_cost - current_cost
            if delta < 0 or random.random() < math.exp(-delta / T):
                current, current_cost = next_path, next_cost
            if next_node == goal:
                break
        return current, current_cost

    def _path_cost(self, path):
        return sum(self.graph[path[i]][path[i + 1]] for i in range(len(path) - 1))
