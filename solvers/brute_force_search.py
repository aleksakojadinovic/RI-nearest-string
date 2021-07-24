import sys
sys.path.append('../utils')
import utils.utils as ut
from .abstractions import *

class BruteForceSolver(AbstractSolver):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def default_config(self) -> dict:
        return dict()

    def name(self) -> str:
        return 'Brute Force DFS Solver'

    def solve(self, problem: CSProblem) -> CSSolution:
        m = problem.m
        alphabet = problem.alphabet
        strings = problem.strings

        q = ['']
        min_hamming = float('inf')
        min_string = None

        iterations = 0
        while q:
            iterations += 1
            curr_string = q.pop()
            curr_string_length = len(curr_string)
            if curr_string_length == m:
                curr_string_score = ut.problem_metric(curr_string, strings)
                if curr_string_score < min_hamming:
                    min_hamming = curr_string_score
                    min_string = curr_string
                continue
            q += [curr_string + next_letter for next_letter in alphabet]

        return CSSolution(min_string, min_hamming, {'iterations': iterations})
    
