import math
import random
from math import exp
from heapq import heappush, heappop

class Graph:
    """Simple undirected, weighted graph."""
    def __init__(self, edges):
        self.edges = edges

    def neighbors(self, state):
        return [n for n, _ in self.edges.get(state, [])]

    def cost(self, a, b):
        for nbr, c in self.edges.get(a, []):
            if nbr == b:
                return c
        raise KeyError(f"No edge {a} → {b}")

class RomaniaProblem:
    """Search problem on the Romania map."""
    def __init__(self, initial, goal, graph, coord):
        self.initial = initial
        self.goal = goal
        self.graph = graph
        self.coord = coord

    def successors(self, state):
        for nbr, c in self.graph.edges.get(state, []):
            yield nbr, c

    def h(self, state):
        x1, y1 = self.coord[state]
        x2, y2 = self.coord[self.goal]
        return math.hypot(x2 - x1, y2 - y1)

class Node:
    def __init__(self, state, parent=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.path_cost = path_cost

    def expand(self, problem):
        for s2, cost in problem.successors(self.state):
            yield Node(s2, self, self.path_cost + cost)

    def solution_path(self):
        node, path = self, []
        while node:
            path.append(node.state)
            node = node.parent
        return list(reversed(path))

def exp_schedule(k=20, lam=0.005, limit=1000):
    def schedule(t):
        return k * exp(-lam * t) if t < limit else 0
    return schedule

def best_first_graph_search(problem, f):
    frontier = []
    entry_finder = {}
    start = Node(problem.initial, path_cost=0)
    heappush(frontier, (f(start), start))
    entry_finder[start.state] = start.path_cost
    explored = set()
    while frontier:
        _, node = heappop(frontier)
        if node.state == problem.goal:
            return node
        explored.add(node.state)
        for child in node.expand(problem):
            if (child.state not in explored and
                (child.state not in entry_finder or child.path_cost < entry_finder[child.state])):
                entry_finder[child.state] = child.path_cost
                heappush(frontier, (f(child), child))
    return None

def greedy_best_first_search(problem):
    return best_first_graph_search(problem, lambda n: problem.h(n.state))

def astar_search(problem):
    return best_first_graph_search(problem, lambda n: n.path_cost + problem.h(n.state))

def hill_climbing(problem):
    current = Node(problem.initial)
    while True:
        neighbors = list(current.expand(problem))
        if not neighbors:
            return current
        best = min(neighbors, key=lambda n: problem.h(n.state))
        if problem.h(best.state) >= problem.h(current.state):
            return current
        current = best

def simulated_annealing(problem, schedule=exp_schedule()):
    current = Node(problem.initial)
    for t in range(1, 10000):
        T = schedule(t)
        if T == 0:
            return current
        neighbors = list(current.expand(problem))
        if not neighbors:
            return current
        next_choice = random.choice(neighbors)
        delta_e = problem.h(current.state) - problem.h(next_choice.state)
        if delta_e > 0 or random.random() < math.exp(delta_e / T):
            current = next_choice
    return current

class SimpleProblemSolvingAgent:
    _roads = {
        'Arad':     [('Zerind',75), ('Sibiu',140), ('Timisoara',118)],
        'Zerind':   [('Arad',75), ('Oradea',71)],
        'Oradea':   [('Zerind',71), ('Sibiu',151)],
        'Timisoara':[('Arad',118), ('Lugoj',111)],
        'Lugoj':    [('Timisoara',111), ('Mehadia',70)],
        'Mehadia':  [('Lugoj',70), ('Dobreta',75)],
        'Dobreta':  [('Mehadia',75), ('Craiova',120)],
        'Sibiu':    [('Arad',140), ('Oradea',151), ('Fagaras',99), ('Rimnicu Vilcea',80)],
        'Rimnicu Vilcea':[('Sibiu',80), ('Craiova',146), ('Pitesti',97)],
        'Craiova':  [('Dobreta',120), ('Rimnicu Vilcea',146), ('Pitesti',138)],
        'Fagaras':  [('Sibiu',99), ('Bucharest',211)],
        'Pitesti':  [('Rimnicu Vilcea',97), ('Craiova',138), ('Bucharest',101)],
        'Bucharest':[('Fagaras',211), ('Pitesti',101), ('Giurgiu',90), ('Urziceni',85)],
        'Giurgiu':  [('Bucharest',90)],
        'Urziceni': [('Bucharest',85), ('Hirsova',98), ('Vaslui',142)],
        'Hirsova':  [('Urziceni',98), ('Eforie',86)],
        'Eforie':   [('Hirsova',86)],
        'Vaslui':   [('Urziceni',142), ('Iasi',92)],
        'Iasi':     [('Vaslui',92), ('Neamt',87)],
        'Neamt':    [('Iasi',87)]
    }
    _coords = {
        'Arad': (91,492), 'Bucharest': (400,327), 'Craiova': (253,288),
        'Dobreta': (165,299), 'Eforie': (562,293), 'Fagaras': (305,449),
        'Giurgiu': (375,270), 'Hirsova': (534,350), 'Iasi': (473,506),
        'Lugoj': (165,379), 'Mehadia': (168,339), 'Neamt': (406,537),
        'Oradea': (131,571), 'Pitesti': (320,368), 'Rimnicu Vilcea': (233,410),
        'Sibiu': (207,457), 'Timisoara': (94,410), 'Urziceni': (456,350),
        'Vaslui': (509,444), 'Zerind': (108,531)
    }

    def __init__(self, start, goal):
        self.graph = Graph(SimpleProblemSolvingAgent._roads)
        self.problem = RomaniaProblem(start, goal, self.graph, SimpleProblemSolvingAgent._coords)

    def run_greedy(self):
        return greedy_best_first_search(self.problem)

    def run_astar(self):
        return astar_search(self.problem)

    def run_hill_climbing(self):
        return hill_climbing(self.problem)

    def run_simulated_annealing(self):
        return simulated_annealing(self.problem)
