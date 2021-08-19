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
    # demonstration_packet = Benchmarker.get_benchmark_packet({'alphabet': ['0', '1'], 'n':10},
    #                                                         target_param_range=range(2, 10),
    #                                                         target_param_name='String length')
    #
    # Benchmarker.save_benchmark_packet(demonstration_packet, 'bps')
    # demonstration_packet = Benchmarker.load_benchmark_packet('bps/bp_String length_2-9')
    # df = Benchmarker.test_solver_against_problems(GeneticSolver(), demonstration_packet)
    # df.to_csv("benchmarking_results/demonstration.csv")
    pass


























