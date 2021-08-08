import math
import numpy as np
from itertools import combinations

import pandas as pd

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution

import cvxopt

def check_constraint(x, lhs, rhs, sign):
    if sign == '=':
        return np.dot(lhs, x) == rhs
    return np.dot(lhs, x) <= rhs

def check_all_constraints(x, lhss, rhss, signs):
    return all(check_constraint(x, lhs, rhs, sign) for lhs, rhs, sign in zip(lhss, rhss, signs))


def solve_zero_one_(self, lhs, rhs, signs):

    pass

def same_idx_list(strs):
    if not strs:
        return []

    return [j for j in range(len(strs[0])) if all(s[j] == strs[0][j] for s in strs)]


def chi(strings, i, j, a):
    if strings[i][j] == a:
        return 0
    return 1


class LiMaWangPTASSolver(AbstractSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def name(self) -> str:
        return 'PTAS1'

    def get_default_config(self) -> dict:
        return {'r_frac': 0.5}

    def solve_(self, problem: CSProblem) -> CSSolution:
        original_string_set = problem.strings
        alphabet = problem.alphabet
        m = problem.m
        n = problem.n

        r_frac = self.config['r_frac']
        r = min(math.floor(r_frac*problem.n), n)

        for subset_index_list in combinations(range(n), r):
            subset_strings = [original_string_set[i] for i in subset_index_list]
            print(f'Considering the following string subset: {subset_strings}')
            Q = same_idx_list(subset_strings)
            P = [j for j in range(m) if j not in Q]

            # Now we must construct a zero-one programming problem
            # The target variables are binary variables of form x_j = a for every a in alphabet and for every j in P
            # meaning there will be exactly |P| * |A| variables
            # If we order them as follows: x_p0 = a0, x_p0 = a1, ... x_p0 = a|A|, x_p1 = a0, x_p1 = a1, ... x_p1 = a|A|, ....... x_p|P| = a0, x_p|P| = a1, ... x_p|P| = a|A|
            # then for the LP variable at position i, we can reconstruct it's meaning as follows:
            # p_index, alphabet_index = np.unravel_indices(i, (len(P), len(A)))

            # First set of conditions will tell us that every p-position can correspond to exactly one alpabet letter
            # meaning for every p-position we need a constraint that sum of its alphabet indicators must be 1
            # meaning
            # for p-position 0 we shall have
            #   (x_p0 = a0) + (x_p0 = a1) + .... + (x_p0 = a|A|) = 1

            print(f'|P| = {len(P)}')
            print(f'|A| = {len(alphabet)}')

            first_part_lp_lhs = np.zeros((len(P), len(P) * len(alphabet)))
            first_part_lp_rhs = np.ones(len(P))
            for lp_row_idx in range(len(P)):
                first_part_lp_lhs[lp_row_idx][lp_row_idx*len(alphabet):(lp_row_idx+1)*len(alphabet)] = np.ones(len(alphabet))

            # print(f'First part LP lhs: ')
            # print(first_part_lp_lhs)
            # print(f'First part LP rhs: ')
            # print(first_part_lp_rhs)

            second_part_lp_lhs = np.zeros((n, len(P)*len(alphabet)))

            for i in range(n):
                coeffs = np.zeros(len(P) * len(alphabet))
                for j in range(len(P)):
                    for alphabet_index in range(len(alphabet)):
                        actual_coeff_idx = j*len(alphabet) + alphabet_index
                        coeffs[actual_coeff_idx] += chi(problem.strings, i, j, alphabet[alphabet_index])
                second_part_lp_lhs[i] = coeffs

            first_part_lp_lhs_extended = np.append(first_part_lp_lhs, np.zeros(len(P)).reshape(-1, 1), axis=1)
            first_part_lp_rhs_extended = first_part_lp_rhs

            second_part_lp_lhs_extended = np.append(second_part_lp_lhs, -np.ones(n).reshape(-1, 1), axis=1)
            second_part_lp_rhs_extended = -np.array([utils.hamming_distance_is(problem.strings[i], problem.strings[Q[0]], Q) for i in range(n)])

            final_lp_lhs = np.vstack((first_part_lp_lhs_extended, second_part_lp_lhs_extended))
            final_lp_rhs = np.append(first_part_lp_rhs_extended, second_part_lp_rhs_extended)
            lp_signs = ['=' for _ in range(len(P))] + ['<=' for _ in range(n)]

            print(f'LPl:')
            print(pd.DataFrame(final_lp_lhs))
            print(f'LPr:')
            print(pd.DataFrame(final_lp_rhs))
            print(f'Signs:')
            print(pd.DataFrame(lp_signs))







            break

            # The first part of this LP problem will have
            # |P| * |A| variables and |P| constraints












        return CSSolution('asd', 4)