import math
import random
import sys
from typing import List
import numpy as np
from itertools import combinations
from tqdm import tqdm
import utils
from abstractions import AbstractSolver, CSProblem, CSSolution
from scipy.optimize import linprog

from solvers.ptas.lp.enumeration_solver import solve_by_force
from solvers.ptas.lp.lp_relaxation_solver import solve_by_lp_relaxation


class LiMaWangPTASSolver(AbstractSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def name(self) -> str:
        return 'PTAS1'

    def get_default_config(self) -> dict:
        return {'r': 4}

    def solve_(self, problem: CSProblem) -> CSSolution:
        original_string_set = problem.strings
        alphabet = problem.alphabet
        m = problem.m
        n = problem.n

        logm = math.log2(m)

        r = self.config['r']

        total_iters = math.factorial(n) // math.factorial(r) // math.factorial(n - r)
        best_non_trivial_string, best_non_trivial_score = None, m

        times_lp = 0
        times_force = 0

        for i, subset_index_list in tqdm(enumerate(combinations(range(n), r)), total=total_iters):
            subset_strings = [original_string_set[i] for i in subset_index_list]
            Q = utils.Q_all(subset_strings)
            P = [j for j in range(m) if j not in Q]
            k = len(P)

            if k <= logm:
                solve_func = solve_by_force
                times_force += 1
            else:
                solve_func = solve_by_lp_relaxation
                times_lp += 1
            s_p = solve_func(P, Q, alphabet, m, n, original_string_set, subset_strings[0])
            if s_p is None:
                continue
            s_p_metric = utils.problem_metric(s_p, original_string_set)
            if s_p_metric <= best_non_trivial_score:
                best_non_trivial_score = s_p_metric
                best_non_trivial_string = s_p

        best_trivial_string, best_trivial_score = None, m
        for s in problem.strings:
            met = utils.problem_metric(s, problem.strings)
            if met <= best_trivial_score:
                best_trivial_score = met
                best_trivial_string = s

        if best_non_trivial_string is None:
            return CSSolution(best_trivial_string, best_trivial_score, problem)

        if best_non_trivial_score < best_trivial_score:
            return CSSolution(best_non_trivial_string, best_non_trivial_score, problem, extra={'times_lp': times_lp, 'times_force': times_force})

        return CSSolution(best_trivial_string, best_trivial_score, problem, extra={'times_lp': times_lp, 'times_force': times_force})
