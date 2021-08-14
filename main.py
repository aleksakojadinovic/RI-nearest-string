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
    problem = loader.load_csp('csps/2-10-250-1-0.csp')


    # problem = CSProblem.from_file('examples/example3.txt')

    # print(StringSearchSolver().solve(problem).measure)

    p = random_problem(10, ['a', 'b', 'c'], 9)
    lmw = LiMaWangPTASSolver()
    r_range = list(range(2, int(p.n / 2)))
    measures = []
    for r in r_range:
        lmw.edit_conf('r', r)
        s = lmw.solve(p)
        measures.append(s.measure)

    for m in measures:
        print(m)

    print(PruningSolver().solve(p))















