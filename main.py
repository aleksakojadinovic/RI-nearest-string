import utils.utils as ut
from solvers.brute_force_search import brute_force_dfs
from solvers.pruning_search import pruning_dfs
from solvers import genetic

from stats.running import simulate_random_over_alphabet_size
from stats.compare import compare_against_range
from generators.random_generator import random_problems_over_alph_size
from generators.string_generator import StringGenerator
import solvers.lp as lp

import matplotlib.pyplot as plt

if __name__ == '__main__':
    input_file = 'examples/ex1.txt'
    problem = ut.read_from_file(input_file)

    pres = pruning_dfs(problem)
    print(f'Pruning dfs:')
    print(F'Best string is {pres["best_string"]} with score {pres["best_score"]}')

    print(f'Genetic: ')
    print('')
    genetic.genetic_solver(problem)
    
    





     

