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

    solvers = [ PruningSolver()
                               .expect(reference_solution)
                               ,
                GeneticSolver()
                               .edit_conf('MAX_ITERS', 5000)
                               .edit_conf('MUT', 0.30)
                               .edit_conf('POP_SIZE', 500)
                               .expect(reference_solution)
                               ,
                StringSearchSolver()
                               .expect(reference_solution)
                               ]
    results = analyze.compare_on_single_problem(solvers, problem)
    for s, r in zip(solvers, results):
        print(f'{s.name()}')        
        print(f'\t time: {r["elapsed"]} s')
        print(f'\t measure: {r["solution"].measure}')
        if s.wrong_flag is None:
            print(f'\t correct: unknown')
        else:
            print(f'\t correct: {not s.wrong_flag}')
    plt.show()

    



    

    



    

    
    
    

    





     


