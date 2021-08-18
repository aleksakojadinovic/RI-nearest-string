import math
import sys
from typing import Tuple

from scipy.optimize import linprog

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution
from solvers.exact.pruning_search import PruningSolver
from itertools import combinations

from solvers.ptas.lp.enumeration_solver import solve_by_force
from solvers.ptas.lp.lp_relaxation_solver import solve_by_lp_relaxation


def yank(s, I):
    return ''.join(c for i, c in enumerate(s) if i in I)

class SimplePTASSolver(AbstractSolver):
    def name(self) -> str:
        return 'Simple PTAS Solver (Li et al.)'

    def get_default_config(self) -> dict:
        return {
            'epsilon': 1.1,
            'sigma': 2
        }

    def solve_(self, problem: CSProblem) -> Tuple[str, dict]:
        m, n, strings, alphabet = problem.m, problem.n, problem.strings, problem.alphabet


        i, j = max(combinations(range(n), 2), key=lambda coords: utils.hamming_distance(strings[coords[0]], strings[coords[1]]))

        si = strings[i]
        sj = strings[j]
        P = utils.P(si, sj)
        Q = utils.Q(si, sj)

        k = len(P) # Number of positions that they disagree on
        epsilon = self.config['epsilon']
        sigma   = self.config['sigma']

        solve_func = solve_by_lp_relaxation
        lp_used = True

        decision_measure = (6*math.log(sigma*m)) // (epsilon**2)

        if k <= decision_measure:
            solve_func = solve_by_force
            lp_used = False

        # print(f'Decision: |P| = {k}', file=sys.stderr)
        # print(f'Measure = {decision_measure}', file=sys.stderr)
        # print(f'Meaning {"FORCE" if not lp_used else "LP"}', file=sys.stderr)

        ss = solve_func(P, Q, alphabet, m, n, strings, si)
        if ss is None:
            # print('not stonks?')
            return si, {'lp_used': lp_used, 'orig': True}

        new_sol, new_sol_metric = ss

        # print(f'Found sol: {new_sol}')

        if new_sol_metric < k:
            return new_sol, {'lp_used': lp_used, 'orig': False}
        return si, {'lp_used': lp_used, 'orig': True}





