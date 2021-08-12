import random

import matplotlib.pyplot as plt

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
    # problem = loader.load_csp('csps/20-50-10000-5-9.csp')


    problem = CSProblem.from_file('examples/example2.txt')

    LiMaWangPTASSolver().solve(problem)













