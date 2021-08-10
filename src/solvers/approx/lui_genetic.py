import random

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution
from generators.random_generator import random_string
import math

def mutate(s, rate, possible_vals):
    r = random.random()
    if r <= rate:
        idx = random.randint(0, len(s) - 1)
        rnd_val = None
        while True:
            rnd_val = random.choice(possible_vals)
            if rnd_val != s[idx]:
                break
        return s[:idx] + rnd_val + s[idx + 1:]
    return s





class LuiEtAlGeneticSolver(AbstractSolver):
    def name(self) -> str:
        return 'Genetic algorithm solver (Liu et al.)'

    def get_default_config(self) -> dict:
        return {
            'MAX_ITERS': 250,
            'POP_SIZE': 10,
            'MUTATION_RATE': 0.05,
            'TOURNAMENT_SIZE': 3
        }

    def solve_(self, problem: CSProblem) -> CSSolution:
        m, n, alphabet, strings = problem.m, problem.n, problem.alphabet, problem.strings
        miters, pop_size, mutation_rate = self.config['MAX_ITERS'], self.config['POP_SIZE'], self.config['MUTATION_RATE']

        selection_size = math.floor(pop_size / 2)
        pop_index_list = list(range(pop_size))
        population = [random_string(alphabet, m) for _ in range(pop_size)]
        fitnesses  = [utils.problem_metric(p, strings) for p in population]

        for iteration in range(miters):
            # Perform selection
            select_units_indices_ = []
            for _ in range(selection_size):
                select_units_indices_.append(random.choices(pop_index_list, k=1, weights=fitnesses)[0])

            new_units_ = []
            new_units_fitnesses_ = []
            for _ in range(selection_size):
                [parent_idx_1, parent_idx_2] = random.choices(select_units_indices_, k=2)
                break_point = random.randint(1, m-1)
                child_1 = population[parent_idx_1][:break_point] + population[parent_idx_2][break_point:]
                child_2 = population[parent_idx_2][:break_point] + population[parent_idx_1][break_point:]

                child_1 = mutate(child_1, mutation_rate, alphabet)
                child_2 = mutate(child_2, mutation_rate, alphabet)

                new_units_.append(child_1)
                new_units_.append(child_2)
                new_units_fitnesses_.append(utils.problem_metric(child_1, strings))
                new_units_fitnesses_.append(utils.problem_metric(child_2, strings))



            population = population + new_units_
            fitnesses = fitnesses + new_units_fitnesses_

            sorted_entries = list(sorted(zip(population, fitnesses), key=lambda x: x[1]))
            population = [a for a, b in sorted_entries]
            fitnesses  = [b for a, b in sorted_entries]
            population, fitnesses = population[:pop_size], fitnesses[:pop_size]

        best_unit, best_unit_metric = min(zip(population, fitnesses), key=lambda x: x[1])

        return CSSolution(best_unit, best_unit_metric)