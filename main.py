from solvers.pruning_search import PruningSolver
import utils.utils as ut
from solvers.abstractions import *
from solvers.brute_force_search import *


import matplotlib.pyplot as plt

if __name__ == '__main__':
    input_file = 'examples/ex1.txt'
    problem = CSProblem.from_file(input_file)
    print(problem)


    # brute_force_solver = BruteForceSolver()
    # brute_force_solver.solve(problem)

    pruning_solver = PruningSolver()
    timed_solution = pruning_solver.run_and_time(problem)

    print(timed_solution['solution'])
    print(timed_solution['elapsed'])
    

    
    

    





     

