from typing import Tuple

import utils
from abstractions import AbstractSolver, CSProblem, CSSolution
from generators.string_generator import StringGenerator

class LexSearchSolver(AbstractSolver):
    def name(self) -> str:
        return 'Lex search solver'

    def get_default_config(self) -> dict:
        return {}

    def solve_(self, problem: CSProblem) -> Tuple[str, dict]:
        best_score = problem.m
        best_string = None
        for s in StringGenerator(problem.alphabet, problem.m):
            sm = utils.problem_metric(s, problem.strings)
            if sm <= best_score:
                best_score = sm
                best_string = s
        return best_string, None