import math
import random
import heapq
from collections import deque

romania_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138},
    'Rimnicu': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Hirsova': 98, 'Vaslui': 142},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87}
}

city_coordinates = {
    'Arad': (91, 492), 'Zerind': (108, 531), 'Oradea': (123, 567), 'Sibiu': (207, 457),
    'Timisoara': (94, 410), 'Lugoj': (165, 379), 'Mehadia': (168, 339), 'Drobeta': (165, 299),
    'Craiova': (235, 293), 'Rimnicu': (233, 410), 'Fagaras': (305, 449), 'Pitesti': (320, 368),
    'Bucharest': (375, 270), 'Giurgiu': (375, 227), 'Urziceni': (456, 350), 'Hirsova': (465, 400),
    'Eforie': (480, 417), 'Vaslui': (509, 444), 'Iasi': (574, 446), 'Neamt': (540, 450)
}

def heuristic(city1, city2='Bucharest'):
    x1, y1 = city_coordinates[city1]
    x2, y2 = city_coordinates[city2]
    return math.hypot(x2 - x1, y2 - y1)

def greedy_best_first_search(start, goal):
    frontier = [(heuristic(start, goal), start)]
    visited = set()
    parent = {start: None}
    while frontier:
        _, current = heapq.heappop(frontier)
        if current == goal:
            return reconstruct_path(parent, current)
        visited.add(current)
        for neighbor in romania_map.get(current, {}):
            if neighbor not in visited:
                parent[neighbor] = current
                heapq.heappush(frontier, (heuristic(neighbor, goal), neighbor))
    return None

def a_star_search(start, goal):
    frontier = [(heuristic(start, goal), 0, start)]
    parent = {start: None}
    g_costs = {start: 0}
    while frontier:
        _, g, current = heapq.heappop(frontier)
        if current == goal:
            return reconstruct_path(parent, current)
        for neighbor, cost in romania_map[current].items():
            new_g = g + cost
            if neighbor not in g_costs or new_g < g_costs[neighbor]:
                g_costs[neighbor] = new_g
                f = new_g + heuristic(neighbor, goal)
                parent[neighbor] = current
                heapq.heappush(frontier, (f, new_g, neighbor))
    return None

def hill_climbing(start, goal):
    current = start
    path = [current]
    visited = {current}
    while current != goal:
        neighbors = [(heuristic(n, goal), n) for n in romania_map[current] if n not in visited]
        if not neighbors:
            break
        next_city = min(neighbors)[1]
        if heuristic(next_city, goal) >= heuristic(current, goal):
            break
        current = next_city
        visited.add(current)
        path.append(current)
    return path if current == goal else None

def simulated_annealing(start, goal, schedule=lambda t: max(0.01, 0.99 ** t)):
    current = start
    current_path = [current]
    t = 0
    while True:
        T = schedule(t)
        if T <= 0:
            break
        neighbors = list(romania_map[current].keys())
        if not neighbors:
            break
        next_city = random.choice(neighbors)
        delta_e = heuristic(current, goal) - heuristic(next_city, goal)
        if delta_e > 0 or random.random() < math.exp(delta_e / T):
            current = next_city
            current_path.append(current)
        if current == goal:
            return current_path
        t += 1
    return None

def reconstruct_path(parents, end):
    path = deque()
    while end:
        path.appendleft(end)
        end = parents[end]
    return list(path)
