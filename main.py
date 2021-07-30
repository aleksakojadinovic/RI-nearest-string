import utils.utils as ut
from generators.string_generator import StringGenerator, StringIterator
from solvers.pruning_search import PruningSolver
from solvers.abstractions import *
from solvers.brute_force_search import *
from solvers.stringsearch import StringSearchSolver
from solvers.genetic import GeneticSolver
import stats.compare as analyze
from generators import random_generator

import matplotlib.pyplot as plt

if __name__ == '__main__':
    input_file = 'examples/ex2.txt'
    problem = CSProblem.from_file(input_file)
    print(problem)

    reference_solution = CSSolution('', 2)

    analyze.compare_on_single_problem([PruningSolver().expect(reference_solution), GeneticSolver().expect(reference_solution), StringSearchSolver().expect(reference_solution)], problem)

    



    

    



    

    
    
    

    





     


