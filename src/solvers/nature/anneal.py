import math
import random

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution
from generators.random_generator import random_string


class SimulatedAnnealingSolver(AbstractSolver):
    def name(self) -> str:
        return 'Simmulated Annealing Solver (Liu et al.)'

    def get_default_config(self) -> dict:
        return {
            'L': 10,
            'GAMMA': 0.9,
            'MAX_ITERS': 250
        }

    def solve_(self, problem: CSProblem) -> CSSolution:
        m, n, strings, alphabet = problem.m, problem.n, problem.strings, problem.alphabet

        gamma = self.config['GAMMA']
        L = self.config['L']
        max_iters = self.config['MAX_ITERS']
        T = m/2

        u = random_string(alphabet, m)
        u_metric = utils.problem_metric(u, strings)

        for iteration in range(max_iters):
            for _ in range(L):
                # random_point = random.randint(1, m - 1)
                # u_prime = u[random_point:] + u[:random_point]
                u_prime = random_string(alphabet, m)
                u_prime_metric = utils.problem_metric(u_prime, strings)

                delta = u_prime_metric - u_metric
                if delta <= 0 or (delta > 0 and math.exp(-delta/T) > random.random()):
                    u = u_prime
                    u_metric = u_prime_metric
            T *= gamma

        return CSSolution(u, u_metric, problem)