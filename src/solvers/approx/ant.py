import random
import time

import numpy as np
import pandas as pd
from tqdm import tqdm

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
            'RHO': 0.1
        }


    def solve_(self, problem: CSProblem) -> CSSolution:
        m, n, alphabet, strings = problem.m, problem.n, problem.alphabet, problem.strings
        A = len(alphabet)
        rho = self.config['RHO']
        colony_size = self.config['COLONY_SIZE']



        global_best_ant = None
        global_best_metric = m

        INNER_TIME_SUM_ = 0
        INNER_TIME_COUNTER_ = 0

        ants = np.full((colony_size, m), '')
        world_trails = np.full((m, A), 1 / A)



        for iteration in range(self.config['MAX_ITERS']):
            local_best_ant = None
            local_best_metric = m
            for ant_idx in range(colony_size):

                for next_character_index in range(m):
                    ants[ant_idx][next_character_index] = random.choices(alphabet, weights=world_trails[next_character_index], k=1)[0]

                ant_metric = utils.problem_metric(ants[ant_idx], strings)

                if ant_metric < local_best_metric:
                    local_best_metric = ant_metric
                    local_best_ant = ants[ant_idx]

            # First we perform pheromone evaporation
            for i in range(m):
                for j in range(A):
                    world_trails[i][j] = world_trails[i][j] * (1 - rho)

            # Now, using the elitist strategy, only the best ant is allowed to update his pheromone trails
            best_ant_ys = (alphabet.index(a) for a in local_best_ant)
            best_ant_xs = range(m)

            for x, y in zip(best_ant_xs, best_ant_ys):
                world_trails[x][y] = world_trails[x][y] + (1 - local_best_metric / m)

            if local_best_metric < global_best_metric:
                global_best_metric = local_best_metric
                global_best_ant = local_best_ant

        print(f'counter: {INNER_TIME_COUNTER_}')
        return CSSolution(''.join(global_best_ant), global_best_metric, extra={'INNER_TIME_SUM_': INNER_TIME_SUM_})







