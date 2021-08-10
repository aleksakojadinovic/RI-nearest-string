import random
import utils
from abstractions import AbstractSolver, CSProblem, CSSolution
from tqdm import tqdm

class AntColonySolver(AbstractSolver):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


    def name(self) -> str:
        return 'Ant Colony Solver'

    def get_default_config(self) -> dict:
        return {
            'MAX_ITERS': 250,
            'COLONY_SIZE': 10,
            'RHO': 0.1
        }


    def solve_(self, problem: CSProblem) -> CSSolution:
        m, n, alphabet, strings = problem.m, problem.n, problem.alphabet, problem.strings
        A = len(alphabet)
        rho = self.config['RHO']
        colony_size = self.config['COLONY_SIZE']

        global_best_ant = None
        global_best_metric = m

        world_trails = [[1.0 / A for _ in range(A)] for _ in range(m)]

        miters = self.config['MAX_ITERS']
        for iteration in range(miters):
            local_best_ant = None
            local_best_metric = m
            for ant_idx in range(colony_size):
                ant = ''.join(random.choices(alphabet, weights=world_trails[next_character_index], k=1)[0] for next_character_index in range(m))
                ant_metric = utils.problem_metric(ant, strings)

                if ant_metric < local_best_metric:
                    local_best_metric = ant_metric
                    local_best_ant = ant

            # First we perform pheromone evaporation
            for i in range(m):
                for j in range(A):
                    world_trails[i][j] = world_trails[i][j] * (1 - rho)

            # Now, using the elitist strategy, only the best ant is allowed to update his pheromone trails
            best_ant_ys = (alphabet.index(a) for a in local_best_ant)
            best_ant_xs = range(m)

            for x, y in zip(best_ant_xs, best_ant_ys):
                world_trails[x][y] = world_trails[x][y] + (1 - 1.0*local_best_metric / m)

            if local_best_metric < global_best_metric:
                global_best_metric = local_best_metric
                global_best_ant = local_best_ant
        return CSSolution(''.join(global_best_ant), global_best_metric)







