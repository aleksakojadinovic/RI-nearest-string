import pstats
import random
import time
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
from tqdm import tqdm

import utils
from abstractions import CSProblem, CSPLoader, CSSolution
from generators.random_generator import generate_solvable_problem, random_alphabet, random_problem
from solvers.exact.brute_force_search import BruteForceSolver
from solvers.exact.lex_search import LexSearchSolver
from solvers.nature.ant import AntColonySolver
from solvers.nature.genetic import LuiEtAlGeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.ptas.li_ma_wang_ptas import LiMaWangPTASSolver
from solvers.ptas.simple_ptas import SimplePTASSolver
from stats.compare import compare_on_single_problem
from stats.experimental import Benchmarker

import pandas as pd
import cProfile

if __name__ == '__main__':
    sols_path = 'results_csp_rnd.csv'

    # loader = CSPLoader('../results_csp_rnd.csv')
    # problem = loader.load_csp('csps/2-10-250-2-7.csp')



    problem = CSProblem.from_file('examples/example2.txt')
    print(problem)







    # print(utils.problem_metric(s["solution"].solution, problem.strings))


























