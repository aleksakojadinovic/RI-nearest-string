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

from concurrent.futures import ThreadPoolExecutor

def same_idx_list(strs):
    if not strs:
        return []
    return [j for j in range(len(strs[0])) if all(s[j] == strs[0][j] for s in strs)]

def diff_idx_list(strs):
    if not strs:
        return []
    return [j for j in range(len(strs[0])) if all(s[j] != strs[0][j] for s in strs)]

def chi(strings, i, j, a):
    if strings[i][j] == a:
        return 0
    return 1

def sat(s, I):
    return ''.join(c for i, c in enumerate(s) if i in I)

def reconstruct_solution(m, Q, A, subset_strings, x_values, alphabet):
    s_prime_as_list = ['' for _ in range(m)]
    p_index = 0
    for x_index in range(m):
        if x_index in Q:
            s_prime_as_list[x_index] = subset_strings[0][x_index]
        else:
            # For each position j we treat all of its a-solutions as the probability distribution
            # for picking the letter a, that is j: (xja1, xja2, ... xja|A|) is the distrib
            candidate_vars = x_values[p_index * A:(p_index + 1) * A]
            # print(f'x_values={x_values}', file=sys.stderr)
            # print(f'candidate vars={candidate_vars}', file=sys.stderr)

            alph_idx = random.choices(range(len(candidate_vars)), k=1, weights=candidate_vars)[0]
            s_prime_as_list[x_index] = alphabet[alph_idx]
            p_index += 1

    s_prime = ''.join(s_prime_as_list)
    return s_prime

def solve_lp_problem_relax(P, Q, alphabet, m, n, original_strings, subset_strings):
    if not Q:
        return None
    LP_T_ = 'float64'

    A = len(alphabet)
    nP = len(P)

    # There are nP*A + 1 variables - nP*A for each xja, and 1 for d
    num_variables = nP*A + 1

    # ======================= CONSTRUCTING THE EQUALITY CONSTRAINTS ========================
    # There are nP constraints with equality
    lp_eq_matrix = np.zeros((nP, num_variables), dtype=LP_T_)
    # For each j we need an "exactly one" constraints
    # The constraint will have ones only within one j-group, and zeros on other positions
    # Therefore we iterate over j-groups
    for i in range(nP):
        left_bound = i*A
        right_bound = (i+1)*A
        lp_eq_matrix[i][left_bound:right_bound] = np.ones(A, dtype=LP_T_)

    # The ds are not in this part and they remain zeros since the matrix was constructed with np.zerps
    # RHS are all ones
    lp_eq_b = np.ones(nP, dtype=LP_T_)

    # ======================= CONSTRUCTING THE INEQUALITY CONSTRAINTS ======================
    # There are n inequality constraints
    # For x_j_a, its absolute position as a variable
    # is j*A + a
    lp_leq_matrix = np.zeros((n, num_variables), dtype=LP_T_)
    # Each of them has -1 coefficient with d, and those correspond to the very last column
    lp_leq_matrix[:, -1] = -np.ones(n, dtype=LP_T_)
    # Other coefficients are chi(i, j, a)
    for i in range(n):
        for a in range(A):
            for j in range(nP):
                actual_var_idx = j*A + a
                lp_leq_matrix[i][actual_var_idx] = chi(original_strings, i, j, alphabet[a])
    # RHS are -d(si|Q, s'|Q)
    lp_leq_b = -np.array([utils.hamming_distance(sat(original_strings[i], Q), sat(subset_strings[0], Q)) for i in range(n)], dtype='int32')

    # Target function is just 'd'
    c = np.zeros(num_variables, dtype=LP_T_)
    c[-1] = 1

    # Every variable must be positive
    lower_bounds = [0.0 for _ in range(num_variables)]
    # xs are constrainted by 1, d is unconstrained above
    upper_bounds: List[any] = [1.0 for _ in range(num_variables-1)] + [None]


    # Now we just plug it into scipy's solver
    sout, serr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = None, None
    lp_solution = linprog(c,
                          A_ub=lp_leq_matrix,
                          b_ub=lp_leq_b,
                          A_eq=lp_eq_matrix,
                          b_eq=lp_eq_b,
                          bounds=list(zip(lower_bounds, upper_bounds)))
    sys.stdout, sys.stderr = sout, serr


    if not lp_solution.success:
        return None

    # print(lp_solution)
    s_prime = reconstruct_solution(m, Q, A, subset_strings, lp_solution.x, alphabet)
    return s_prime

class LiMaWangPTASSolver(AbstractSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def name(self) -> str:
        return 'PTAS1'

    def get_default_config(self) -> dict:
        return {'r': 2}

    def solve_(self, problem: CSProblem) -> CSSolution:
        original_string_set = problem.strings
        alphabet = problem.alphabet
        m = problem.m
        n = problem.n

        r = self.config['r']
        best_string = None
        best_score = m

        for subset_index_list in combinations(range(n), r):
            subset_strings = [original_string_set[i] for i in subset_index_list]
            Q = same_idx_list(subset_strings)
            P = [j for j in range(m) if j not in Q]
            # P = diff_idx_list(subset_strings)

            s_p = solve_lp_problem_relax(P, Q, alphabet, m, n, original_string_set, subset_strings)
            if s_p is None:
                continue
            s_p_metric = utils.problem_metric(s_p, original_string_set)
            if s_p_metric <= best_score:
                best_score = s_p_metric
                best_string = s_p

        # print(f'Best LP sol: {best_score}')


        best_trivial = None
        best_trivial_score = m
        for s in problem.strings:
            met = utils.problem_metric(s, problem.strings)
            if met <= best_trivial_score:
                best_trivial_score = met
                best_trivial = s
        # print(f'Best trivial sol: {best_score}')

        if best_score is None:
            return CSSolution(best_trivial, best_trivial_score)

        if best_score < best_trivial_score:
            return CSSolution(best_string, best_score)

        return CSSolution(best_trivial, best_trivial_score)
