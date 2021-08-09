import matplotlib.pyplot as plt

from abstractions import CSProblem
from solvers.approx.ant import AntColonySolver
from solvers.approx.genetic import GeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.exact.string_search import StringSearchSolver
from solvers.ptas.li_ma_wang_ptas import LiMaWangPTASSolver
from stats.compare import compare_on_single_problem


if __name__ == '__main__':

    input_file = 'csps/2-10-250-1-0.csp'
    problem = CSProblem.from_csp(input_file)

    print(problem)

    tsol = AntColonySolver().edit_conf('MAX_ITERS', 250).edit_conf('COLONY_SIZE', 10).run_and_time(problem)

    print(f"Total time: {tsol['elapsed']}")
    print(f"Inner time: {tsol['solution'].extra['INNER_TIME_SUM_']}")
    print(tsol['solution'])




