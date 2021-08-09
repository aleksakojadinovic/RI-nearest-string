import random
import numpy as np
import pandas as pd

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution

def get_possible_positions(n_rows, n_cols, x, y):
    dvs = [
        (-1, +1), # up right
        ( 0, +1), # right
        (+1, +1)  # down right
    ]
    cs = []
    for dx, dy in dvs:
        nx, ny = x + dx, y + dy
        if 0 <= nx < n_rows and 0 <= ny < n_cols:
            cs.append((nx, ny))

    return cs


def random_pos_in_matrix(n_rows, n_cols):
    return random.randint(0, n_rows - 1), random.randint(0, n_cols - 1)


class AntColonySolver(AbstractSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.evap_function = np.vectorize(lambda x: (1-self.config['RHO'])*x)

    def name(self) -> str:
        pass

    def get_default_config(self) -> dict:
        return {
            'MAX_ITERS': 1000,
            'COLONY_SIZE': 100,
            'EVAPORATION_COEFF': 0.5,
            'RHO': 0.3
        }


    def solve_(self, problem: CSProblem) -> CSSolution:
        m, n, alphabet, strings = problem.m, problem.n, problem.alphabet, problem.strings
        A = len(alphabet)
        world_trails = np.full((A, m), 1/A)

        global_best_ant = None
        global_best_metric = float('inf')

        for iteration in range(self.config['MAX_ITERS']):
            local_best_ant = None
            local_best_metric = float('inf')
            for _ in range(self.config['COLONY_SIZE']):
                # We choose the first letter separately because it makes
                # the loop easier (less ifs)
                # We make the choice based on the first column pheromon levels
                ant = random.choices(alphabet, weights=[world_trails[k][0] for k in range(A)], k=1)[0]
                for next_character_index in range(1, m):
                    ant += random.choices(alphabet, weights=world_trails[:, next_character_index], k=1)[0]



                ant_metric = utils.problem_metric(ant, strings)
                if ant_metric < local_best_metric:
                    local_best_metric = ant_metric
                    local_best_ant = ant

            # First we perform pheromone evaporation
            world_trails = self.evap_function(world_trails)

            # Now, using the elitist strategy, only the best ant is allowed to update his pheromone trails
            best_ant_xs = (alphabet.index(a) for a in local_best_ant)
            best_ant_ys = range(m)

            for x, y in zip(best_ant_xs, best_ant_ys):
                world_trails[x][y] = world_trails[x][y] + (1 - local_best_metric / m)

            if local_best_metric < global_best_metric:
                global_best_metric = local_best_metric
                global_best_ant = local_best_ant

        return CSSolution(global_best_ant, global_best_metric)







