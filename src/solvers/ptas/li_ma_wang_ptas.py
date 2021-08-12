import math
import numpy as np
from itertools import combinations
import utils
from abstractions import AbstractSolver, CSProblem, CSSolution

from ortools.linear_solver import pywraplp

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
        A = len(alphabet)
        for subset_index_list in combinations(range(n), r):
            subset_strings = [original_string_set[i] for i in subset_index_list]
            Q = same_idx_list(subset_strings)
            P = [j for j in range(m) if j not in Q]

            # Now we must construct a zero-one programming problem
            # The target variables are binary variables of form x_j = a for every a in alphabet and for every j in P
            # meaning there will be exactly |P| * |A| variables
            # If we order them as follows: x_p0 = a0, x_p0 = a1, ... x_p0 = a|A|, x_p1 = a0, x_p1 = a1, ... x_p1 = a|A|, ....... x_p|P| = a0, x_p|P| = a1, ... x_p|P| = a|A|
            # then for the LP variable at position i, we can reconstruct its meaning as follows:
            # p_index, alphabet_index = np.unravel_indices(i, (len(P), len(A)))

            # First set of conditions will tell us that every p-position can correspond to exactly one alpabet letter
            # meaning for every p-position we need a constraint that sum of its alphabet indicators must be 1
            # meaning
            # for p-position 0 we shall have
            #   (x_p0 = a0) + (x_p0 = a1) + .... + (x_p0 = a|A|) = 1


            lp_matrix = np.zeros((len(P) + n, len(P)*A+n + 1), dtype='int32')
            for lp_row_idx in range(len(P)):
                lp_matrix[lp_row_idx][lp_row_idx*A:(lp_row_idx+1)*A] = np.ones(A)

            lp_matrix[len(P):, len(P)*A:-1] = np.eye(n)
            for i, lp_row_idx in enumerate(range(len(P), len(P)+n)):
                for j in range(len(P)):
                    for a in range(A):
                        lp_matrix[lp_row_idx][j*A + a] += chi(problem.strings, i, j, alphabet[a])


            lp_matrix[:, -1] = -np.ones(len(P) + n)

            lp_b = np.ones(len(P) + n)
            lp_b[len(P):] = -np.array([utils.hamming_distance(sat(si, Q), sat(subset_strings[0], Q)) for si in problem.strings])


            solver = pywraplp.Solver.CreateSolver('SCIP')
            infinity = solver.infinity()

            problem_variables = [solver.IntVar(0.0, 1.0, f'y_{i}') for i in range(len(P)*A + n + 1)] + [solver.IntVar(0.0, m, 'd')]
            # for i, (row, b) in enumerate(zip(lp_matrix, lp_b)):
            #     constraint = solver.RowConstraint(-infinity, b, '')
            #     for j, coeff in enumerate(row):
            #         _ = problem_variables[j]
            #         constraint.SetCoefficient(problem_variables[j], int(coeff))

            for i, (l, r) in enumerate(zip(lp_matrix, lp_b)):
                constraint = [coeff*var for coeff, var in zip(l, problem_variables)]
                solver.Add(sum(constraint) <= r)
                # solver.Add(sum(coeff*var) <= r for coeff, var in zip(l, problem_variables))

            objective = solver.Objective()
            for j in range(len(P)*A+n + 1):

                objective.SetCoefficient(problem_variables[j], 1 if j == len(P)*A+n else 0)

            objective.SetMinimization()

            status = solver.Solve()

            solution_vector = np.array([int(pv.solution_value()) for pv in problem_variables])
            print(solution_vector)



            break













        return CSSolution('asd', 4)