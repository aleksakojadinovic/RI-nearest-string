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
    input_file = 'csps/2-10-250-1-0.csp'

    loader = CSPLoader('../results_csp_rnd.csv')
    problem = loader.load_csp('csps/2-10-250-1-0.csp')

    # tsol = AntColonySolver().run_and_time(problem)
    # print(f'Total time: {tsol["elapsed"]} s')
    # print(f'Score: {tsol["solution"].measure}')
    # print(f'Info: {tsol["solution"].extra}')


    # TRIALS = 1
    # tsols = [GeneticSolver().edit_conf('MAX_ITERS', 250).edit_conf('MUT', 0.2).run_and_time(problem) for _ in range(TRIALS)]
    # times = [t["elapsed"] for t in tsols]
    # sols  = [t["solution"].measure for t in tsols]
    #
    # avg_time = sum(times)/TRIALS
    # avg_sol = sum(sols)/TRIALS
    #
    # print(f'Average running time: {avg_time} seconds.')
    # print(f'Average string score: {avg_sol}.')
    # print('Average precision:    {:0.2f}%'.format(100*problem.expect / avg_sol))


    # profile = cProfile.Profile()
    # profile.enable()



    for s in [LuiEtAlGeneticSolver(), GeneticSolver()]:
        tsol = s.run_and_time(problem)
        print(f'{s.name()} :')
        print(f'\t{tsol["elapsed"]}')
        print(f'\t{tsol["solution"]}')







