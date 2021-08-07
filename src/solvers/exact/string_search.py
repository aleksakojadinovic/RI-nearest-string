import math
from typing import List
import utils as ut
from abstractions import AbstractSolver, CSProblem, CSSolution
from generators.string_generator import StringGenerator


class ystr(str):
    def __or__(self, index_list):
        return ystr(''.join(c for i, c in enumerate(str(self)) if i in index_list))

    def set_char(self, index, char):
        s = str(self)
        return ystr(s[:index] + char + s[index + 1:])

    def diff_idx(self, other):
        return [i for i, (c1, c2) in enumerate(zip(self, other)) if c1 != c2]

    def same_idx(self, other):
        return [i for i, (c1, c2) in enumerate(zip(self, other)) if c1 == c2]


def string_search_solver(strings, ds, alphabet):
    m = len(strings[0])
    n = len(strings)
    strings = [ystr(s) for s in strings]
    return string_search_solver_(strings, ds, alphabet, m, n)


def string_search_solver_(strings: List[ystr], ds: List[int], alphabet: List[str], m, n):
    s0 = strings[0]
    i0 = None
    for i in range(n):
        curr_str = strings[i]
        if ut.hamming_distance(s0, curr_str) > ds[i]:
            i0 = i
            break

    if i0 is None:
        return s0

    si0 = strings[i0]
    Q = s0.same_idx(si0)
    P = s0.diff_idx(si0)
    # P = [j for j in list(range(0, len(s0))) if j not in Q]

    for t in map(ystr, StringGenerator(alphabet, len(P))):
        if ut.hamming_distance(t, s0 | P) <= ds[0] and ut.hamming_distance(t, si0 | P) <= ds[i0]:
            e1 = min(ds[0] - ut.hamming_distance(t, s0 | P), math.ceil(ds[0] / 2))
            es = [e1] + [ds[i] - ut.hamming_distance(t, strings[i] | P) for i in range(1, len(strings))]
            u = string_search_solver_([s | Q for s in strings], es, alphabet, len(Q), n)
            if u is not None:
                final_str = ''
                for i in range(m):
                    if i in P:
                        final_str += t[P.index(i)]
                    else:
                        final_str += u[Q.index(i)]
                return final_str
    return None


def d_string_search(problem: CSProblem, d: int):
    return string_search_solver(problem.strings, [d for _ in range(problem.n)], problem.alphabet)


def optimize_string_search(problem: CSProblem):
    for best_dist in range(problem.m + 1):
        sol = d_string_search(problem, best_dist)
        if sol is not None:
            score = ut.problem_metric(sol, problem.strings)
            return sol, score
    return None, None


class StringSearchSolver(AbstractSolver):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_default_config(self) -> dict:
        return {}

    def name(self) -> str:
        return 'String search solver'

    def solve_(self, problem: CSProblem) -> CSSolution:
        sol, score = optimize_string_search(problem)
        if sol is None:
            raise ValueError(f'Nesto ne valja u algoritmu :D')
        return CSSolution(sol, score)