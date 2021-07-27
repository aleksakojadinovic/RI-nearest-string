from generators.string_generator import StringGenerator, StringIterator
from solvers.pruning_search import PruningSolver
import utils.utils as ut
from solvers.abstractions import *
from solvers.brute_force_search import *
from solvers.genetic import *

import stats.compare
from generators import random_generator


import matplotlib.pyplot as plt

if __name__ == '__main__':
    # input_file = 'examples/ex1.txt'
    # problem = CSProblem.from_file(input_file)
    # print(problem)


    # brute_force_solver = BruteForceSolver()
    # brute_force_solver.solve(problem)

    # pruning_solver = PruningSolver()
    # pruning_solver.expect(CSSolution('', 6))
    # timed_solution = pruning_solver.run_and_time(problem)
    # print(timed_solution['solution'])

    # print(timed_solution['solution'])
    # print(timed_solution['elapsed'])

    # solver1 = PruningSolver()
    # solver2 = GeneticSolver()
    # solver3 = GeneticSolver()
    # solver3.edit_conf('POP_SIZE', 100)

    # alphabet = random_generator.random_alphabet(5)
    # # num_strings = 20
    # # min_str_size = 3
    # # max_str_size = 10

    # # problems = random_generator.random_problems_over_string_size(alphabet, num_strings,  min_str_size, max_str_size)
    # # stats.compare.compare_on_range_of_problems([solver1, solver2, solver3], problems, list(range(min_str_size, 1 + max_str_size)), 'String size (m)')
    # # plt.show()

    # string_length = 10
    # min_num_strs = 4
    # max_num_strs = 10
    # problems = random_generator.random_problems_over_num_of_strings(alphabet, string_length, min_num_strs, max_num_strs)
    # stats.compare.compare_on_range_of_problems([solver1, solver2, solver3], problems, list(range(min_num_strs, 1 + max_num_strs)), 'Number of strings (n)')

    # plt.show()
    
    alphabet = ['a', 'b', 'c', 'd', 'e']
    a = len(alphabet)
    length = 6

    all_strs = list(StringGenerator(alphabet, length))
    expected = a ** length

    print(f'my: {len(all_strs)} ex: {expected}, good: {len(all_strs) == expected}')


    

    
    
    

    





     

