import matplotlib.pyplot as plt

from abstractions import CSProblem
from solvers.approx.genetic import GeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.exact.string_search import StringSearchSolver
from stats.compare import compare_on_single_problem


if __name__ == '__main__':

    input_file = 'examples/example1.txt'
    problem = CSProblem.from_file(input_file)

    solvers = [PruningSolver(),
               GeneticSolver()
                   .edit_conf('MAX_ITERS', 500)
                   .edit_conf('MUT', 0.30)
                   .edit_conf('POP_SIZE', 500),
               StringSearchSolver()
               ]
    results = compare_on_single_problem(solvers, problem)
    for s, r in zip(solvers, results):
        print(f'{s.name()}')
        print(f'\t time: {r["elapsed"]} s')
        print(f'\t measure: {r["solution"].measure}')
        if r['solution'].correct is None:
            print(f'\t correct: unknown')
        else:
            print(f'\t correct: {r["solution"].correct}')
    plt.show()



