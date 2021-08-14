import pstats
import random
import time
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
from tqdm import tqdm

import utils
from abstractions import CSProblem, CSPLoader
from generators.random_generator import generate_solvable_problem, random_alphabet, random_problem
from solvers.approx.ant import AntColonySolver
from solvers.approx.lui_genetic import LuiEtAlGeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.exact.string_search import StringSearchSolver
from solvers.ptas.li_ma_wang_ptas import LiMaWangPTASSolver
from stats.compare import compare_on_single_problem
from stats.experimental import Benchmarker

import pandas as pd
import cProfile

if __name__ == '__main__':
    sols_path = 'results_csp_rnd.csv'

    loader = CSPLoader('../results_csp_rnd.csv')
    problem = loader.load_csp('csps/2-10-250-1-0.csp')


    # problem = CSProblem.from_file('examples/example3.txt')

    # print(StringSearchSolver().solve(problem).measure)

    # profile = cProfile.Profile()
    # profile.enable()

    lmw = LiMaWangPTASSolver()
    r = 2
    lmw.edit_conf('r', 2)
    s = lmw.run_and_time(problem)
    # profile.disable()
    # profile.dump_stats('profile_out.prof')
    stream = open('profile_out.txt', 'w')
    stats = pstats.Stats('profile_out.prof', stream=stream)
    stats.sort_stats('cumtime')
    # stats.print_stats()

    print(f'Total time: {s["elapsed"]}')

    # def task(i):
    #     time.sleep(2)
    #     print(f'task {i}')
    #
    # with ThreadPoolExecutor(max_workers=128) as tpe:
    #     for i in range(5):
    #         tpe.submit(task, i)
    #         print(f'Task {i} submitted')

























