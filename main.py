import matplotlib.pyplot as plt

from abstractions import CSProblem, CSPLoader
from solvers.approx.ant import AntColonySolver
from solvers.approx.genetic import GeneticSolver
from solvers.approx.lui_genetic import LuiEtAlGeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.exact.string_search import StringSearchSolver
from solvers.ptas.li_ma_wang_ptas import LiMaWangPTASSolver
from stats.compare import compare_on_single_problem

import pandas as pd
import cProfile

if __name__ == '__main__':
    sols_path = 'results_csp_rnd.csv'

    loader = CSPLoader('../results_csp_rnd.csv')
    problem = loader.load_csp('csps/20-50-10000-5-9.csp')

    TRIALS = 1
    tsols = [AntColonySolver().edit_conf('MAX_ITERS', 500).edit_conf('COLONY_SIZE', 75).run_and_time(problem) for _ in range(TRIALS)]
    times = [t["elapsed"] for t in tsols]
    sols  = [t["solution"].measure for t in tsols]

    avg_time = sum(times)/TRIALS
    avg_sol = sum(sols)/TRIALS

    print(f'Average running time: {avg_time} seconds.')
    print(f'Average string score: {avg_sol}.')
    print('Average precision:    {:0.2f}%'.format(100*problem.expect / avg_sol))








