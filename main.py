import matplotlib.pyplot as plt

from abstractions import CSProblem
from solvers.approx.ant import AntColonySolver
from solvers.approx.genetic import GeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.exact.string_search import StringSearchSolver
from solvers.ptas.li_ma_wang_ptas import LiMaWangPTASSolver
from stats.compare import compare_on_single_problem

import cProfile

if __name__ == '__main__':

    input_file = 'csps/2-10-250-1-0.csp'
    problem = CSProblem.from_csp(input_file)

    # tsol = AntColonySolver().run_and_time(problem)
    # print(f'Total time: {tsol["elapsed"]} s')

    profile = cProfile.Profile()
    profile.enable()

    AntColonySolver().solve(problem)

    profile.disable()
    profile.print_stats()





