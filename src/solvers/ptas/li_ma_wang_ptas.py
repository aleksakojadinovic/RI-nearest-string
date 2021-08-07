import math
import numpy as np
from itertools import combinations
from abstractions import AbstractSolver, CSProblem, CSSolution

def same_idx_list(strs):
    if not strs:
        return []

    return [j for j in range(len(strs[0])) if all(s[j] == strs[0][j] for s in strs)]




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

            print(f'|P| = {len(P)}')

            first_part_lp_lhs = np.zeros((len(P), len(P) * len(alphabet)))
            for lp_row_idx in range(len(P)):
                first_part_lp_lhs[lp_row_idx][lp_row_idx*len(alphabet):(lp_row_idx+1)*len(alphabet)] = np.ones(len(alphabet))

            print(f'First part LP: ')
            print(first_part_lp_lhs)

            break

            # The first part of this LP problem will have
            # |P| * |A| variables and |P| constraints












        return CSSolution('asd', 4)