from search import *

def main():
    initial_state = (1, 2, 3, 4, 5, 6, 7, 8, 0)
    goal_state = (8, 7, 6, 5, 4, 3, 2, 1, 0)
    problem = Problem(initial_state, goal_state)
    eightPuzzle = EightPuzzle(problem)
    print(eightPuzzle.find_blank_square(initial_state))
    print(eightPuzzle.actions(initial_state))
    print(eightPuzzle.check_solvability(initial_state))
    print()

    new_state = eightPuzzle.result(initial_state, 'LEFT')
    print(new_state)
    print(eightPuzzle.find_blank_square(new_state))
    print(eightPuzzle.actions(new_state))
    print(eightPuzzle.check_solvability(new_state))
    print()

    new_state = eightPuzzle.result(new_state, 'UP')
    print(new_state)
    print(eightPuzzle.find_blank_square(new_state))
    print(eightPuzzle.actions(new_state))
    print(eightPuzzle.check_solvability(new_state))

if __name__ == "__main__":
    main()