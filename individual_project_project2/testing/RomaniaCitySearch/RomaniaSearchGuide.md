# 🇷🇴 Romania Search Project - Usage Guide
This notebook demonstrates how to use the files in the `RomaniaCitySearch.zip` project.

You can:
- Run the search algorithms
- Visualize the paths
- Test the implementation


```
from search_algorithms import greedy_best_first_search, a_star_search, hill_climbing, simulated_annealing

origin = 'Arad'
destination = 'Bucharest'

print("Greedy Best-First:", greedy_best_first_search(origin, destination))
print("A* Search:", a_star_search(origin, destination))
print("Hill Climbing:", hill_climbing(origin, destination))
print("Simulated Annealing:", simulated_annealing(origin, destination))
```


```
from visualization import draw_path
path = a_star_search("Arad", "Bucharest")
draw_path(path, title="A* Search from Arad to Bucharest")
```


```
# Run unit tests (optional)
!python3 test_search_algorithms.py
```
