import random
import sys
sys.path.append('../utils')
sys.path.append('../generators')
import utils.utils as ut
from generators import random_generator
from .abstractions import *
from tqdm import tqdm

class GeneticSolver(AbstractSolver):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
    
    def default_config(self) -> dict:
        return {'POP_SIZE': 100,
                'MAX_ITERS': 50,
                'TOUR_SIZE': 10,
                'REPR_SIZE': 300,
                'MUT': 0.05}

    def name(self) -> str:
        return 'Genetic algorithm solver'

    def init_pop(self, pop_size, alphabet, length):
        return random_generator.random_strings(self.config['POP_SIZE'], alphabet, length)

    def tournament_selection(self, pop, scores):
        entries = zip(pop, scores)
        selected = random.sample(list(entries), self.config['TOUR_SIZE'])
        (winner, score) = min(selected, key = lambda x: x[1])
        return winner, score

    def perform_selection(self, pop, scores):
        for_reproduction = [self.tournament_selection(pop, scores) for _ in range(self.config['REPR_SIZE'])]
        return for_reproduction

    def get_best(self, pop, scores):
        best_unit = None
        best_score = None
        for p, s in zip(pop, scores):
            if best_unit is None or s < best_score:
                best_score = s
                best_unit = p
        return best_unit, best_score

    def crossover(self, s1, s2):
        break_point = random.randrange(1, len(s1))
        return s1[:break_point] + s2[break_point:]

    
    def mutate(self, s, alphabet):
        random_value = random.random()
        if random_value < self.config['MUT']:
            random_index = random.randrange(len(s))
            while True:
                new_value = random.choice(alphabet)
                if s[random_index] != new_value:
                    break
            s = s[:random_index] + new_value + s[random_index + 1:]
        return s

    def reproduce(self, for_reproduction, strings, alphabet):
        new_gen = []
        new_gen_scores = []
        while len(new_gen) != self.config['POP_SIZE']:
            [(parent1, _), (parent2, _)] = random.sample(for_reproduction, 2)
            new_string = self.crossover(parent1, parent2)
            new_string = self.mutate(new_string, alphabet)
            new_string_score = ut.problem_metric(new_string, strings)

            new_gen.append(new_string)
            new_gen_scores.append(new_string_score)

        return new_gen, new_gen_scores

    def solve_(self, problem: CSProblem) -> CSSolution:
        m = problem.m
        alphabet = problem.alphabet
        strings = problem.strings
        n = problem.n

        current_pop     = self.init_pop(self.config['POP_SIZE'], alphabet, m)
        current_scores  = [ut.problem_metric(s, strings) for s in current_pop]
        best_unit, best_score = self.get_best(current_pop, current_scores)

        for i in range(self.config['MAX_ITERS']):
            for_reproduction = self.perform_selection(current_pop, current_scores)
            new_pop, new_pop_score = self.reproduce(for_reproduction, strings, alphabet)
            curr_best, curr_best_score = self.get_best(new_pop, new_pop_score)
            if curr_best_score < best_score:
                best_unit = curr_best
                best_score = curr_best_score

        return CSSolution(best_unit, best_score)
    
    
    

    

