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

    loader = CSPLoader('../results_csp_rnd.csv')
    problem = loader.load_csp('csps/2-10-250-2-7.csp')

    # n_packet = Benchmarker.get_benchmark_packet({'alphabet': ['a', 'c', 't', 'g'], 'm': 20},
    #                                             target_param_name='n',
    #                                             target_param_range=[25, 50, 75, 100, 125, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500])
    #
    # Benchmarker.save_benchmark_packet(n_packet, 'bps', packet_name_prefix='testing_n')

    # n_packet = Benchmarker.load_benchmark_packet('bps/testing_n_bp_n_25-500')

    # m_packet = Benchmarker.get_benchmark_packet({'alphabet': ['0', '1'], 'n': 10},
    #                                             target_param_range=[25, 50, 75, 100, 125, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500],
    #                                             target_param_name='m')
    #
    # Benchmarker.save_benchmark_packet(m_packet, 'bps', packet_name_prefix='testing_m')
    # m_packet = Benchmarker.get_benchmark_packet({'alphabet': ['a', 'c', 't', 'g'], 'n': 10},
    #                                             target_param_range=[25, 50, 75, 100, 125, 175, 200, 225, 250, 275, 300, 325, 350, 375, 400, 425, 450, 475, 500],
    #                                             target_param_name='m')
    #
    # Benchmarker.save_benchmark_packet(m_packet, 'bps', packet_name_prefix='testing_m')

    # m_packet = Benchmarker.load_benchmark_packet('bps/testing_m_bp_m_25-500')
    # df = Benchmarker.test_solver_against_problems(GeneticSolver(), m_packet)
    # df.to_csv('benchmarking_results/testing_m_genetic_just_in_case.csv')


    # nvm = SimplePTASSolver().run_and_time(CSProblem.from_file('bps/testing_n_bp_n_25-500/50.txt'))
    # print(nvm)

    # a_packet = Benchmarker.get_benchmark_packet({'m': 90, 'n': 10},
    #                                             target_param_range=[10, 20, 30, 40, 50, 60, 70, 80, 90],
    #                                             target_param_name='alphabet_size')
    # #
    # Benchmarker.save_benchmark_packet(a_packet, 'bps', packet_name_prefix='testing_a')

    a_packet = Benchmarker.load_benchmark_packet('bps/testing_a_bp_alphabet_size_10-90')

    df = Benchmarker.test_solver_against_problems(SimplePTASSolver(), a_packet)
    df.to_csv('benchmarking_results/testing_a_ptas.csv')
#

























