from search import *

def fitness(q):
    non_attacking = 0
    for row1 in range(len(q)):
        for row2 in range(row1+1, len(q)):
            col1 = int(q[row1])
            col2 = int(q[row2])
            row_diff = row1 - row2
            col_diff = col1 - col2

            if col1 != col2 and row_diff != col_diff and row_diff != -col_diff:
                non_attacking += 1

    return non_attacking

def main():
    """Initializes population for genetic algorithm
        pop_number  :  Number of individuals in population
        gene_pool   :  List of possible values for individuals
        state_length:  The length of each individual
    """

    population = init_population(100, range(8), 8)
    print(population[:5]) #Display the first 5 individuals. Each individual is a solution state for the 8-Queens Problem

    solution = genetic_algorithm(population, fitness, gene_pool=range(8), f_thres=25)
    print(solution)

    print(fitness(solution))

if __name__ == "__main__":
    main()