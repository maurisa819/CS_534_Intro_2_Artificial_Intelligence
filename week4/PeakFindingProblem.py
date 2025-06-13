from search import *

# directions4 = {'W': (-1, 0), 'N': (0, 1), 'E': (1, 0), 'S': (0, -1)}
# directions8 = dict(directions4)
# directions8.update({'NW': (-1, 1), 'NE': (1, 1), 'SE': (1, -1), 'SW': (-1, -1)})

def main():
    initial = (0, 0)
    grid = [[10, 20, 15], [21, 30, 14], [7, 16, 32]]

    problem = PeakFindingProblem(initial, grid, directions4)

    solutions = [problem.value(simulated_annealing(problem)) for i in range(100)] #Change to 100
    print(solutions)

    solutions = set(solutions)
    print(solutions)

    print(max(solutions))

if __name__ == "__main__":
    main()