import pstats
import random
import time
from concurrent.futures import ThreadPoolExecutor

import matplotlib.pyplot as plt
from tqdm import tqdm

import utils
from abstractions import CSProblem, CSPLoader, CSSolution
from generators import random_generator
from generators.random_generator import generate_solvable_problem, random_alphabet, random_problem
from solvers.exact.brute_force_search import BruteForceSolver
from solvers.exact.lex_search import LexSearchSolver
from solvers.nature.ant import AntColonySolver
from solvers.nature.genetic import GeneticSolver
from solvers.exact.pruning_search import PruningSolver
from solvers.ptas.li_ma_wang_ptas import LiMaWangPTASSolver
from solvers.ptas.simple_ptas import SimplePTASSolver
from stats.compare import compare_on_single_problem
from stats.experimental import Benchmarker

import pandas as pd
import cProfile

if __name__ == '__main__':
    sols_path = 'results_csp_rnd.csv'



    problem = CSProblem(4, 3, ['acct', 'aagt', 'cagt'], ['a', 'c', 't', 'g'])
    print(PruningSolver().run_and_time(problem))
#

























