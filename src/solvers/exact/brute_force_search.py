from typing import Tuple

from abstractions import AbstractSolver, CSProblem, CSSolution
from utils import problem_metric

class BruteForceSolver(AbstractSolver):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_default_config(self) -> dict:
        return {}

    def name(self) -> str:
        return 'Brute Force DFS Solver'

    def solve_(self, problem: CSProblem) -> Tuple[str, dict]:
        m = problem.m
        alphabet = problem.alphabet
        strings = problem.strings

        q = ['']
        min_hamming = float('inf')
        min_string = None
        iterations = 0
        leaves = 0
        while q:
            iterations += 1
            curr_string = q.pop()
            curr_string_length = len(curr_string)
            if curr_string_length == m:
                leaves += 1
                curr_string_score = problem_metric(curr_string, strings)
                if curr_string_score < min_hamming:
                    min_hamming = curr_string_score
                    min_string = curr_string
                continue
            q += [curr_string + next_letter for next_letter in alphabet]

        return min_string, {'iterations': iterations, 'leaves': leaves}