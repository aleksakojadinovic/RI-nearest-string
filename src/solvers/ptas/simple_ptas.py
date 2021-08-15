from scipy.optimize import linprog

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution


class SimplePTASSolver(AbstractSolver):
    def name(self) -> str:
        return 'Simple PTAS Solver (Li et al.)'

    def get_default_config(self) -> dict:
        return {
            'epsilon': 1,
            'sigma': 1
        }

    def solve_(self, problem: CSProblem) -> CSSolution:
        m, n, strings, alphabet = problem.m, problem.n, problem.strings, problem.alphabet

        i_cap = None
        j_cap = None
        max_dist = 0
        for i in range(n):
            for j in range(n):
                dist = utils.hamming_distance(strings[i], strings[j])
                if dist >= max_dist:
                    max_dist = dist
                    i_cap = i
                    j_cap = j

        if max_dist == 0:
            # Max distance between any pair of the input strings is zero,
            # perfect solution (never gonna happen but gotta handle it)
            return CSSolution(strings[0], 0)

        si = strings[i_cap]
        sj = strings[j_cap]
        P = [j for j, (c1, c2) in enumerate(zip(si, sj)) if c1 != c2]
        Q = [j for j, (c1, c2) in enumerate(zip(si, sj)) if c1 == c2]

        k = len(P) # Number of positions that they disagree on

        # We optimize on the disagreeing positions (those in P)
        # min d
        # d(s)



