import json
import time
import sys
from typing import List
sys.path.append('../utils')
from utils.utils import get_alphabet_all

class CSProblem:
    @staticmethod 
    def from_dict(d):
        return CSProblem(d['m'], d['n'], d['strings'], d['alphabet'])
    
    @staticmethod
    def from_file(filepath):
        f = open(filepath, 'r')
        lines = f.read().splitlines()
        lines = (l for l in lines if not l.startswith('#'))
        lines = (l for l in lines if l)
        lines = list(lines)
        if not lines:
            raise ValueError(f'Empty file.')
        n = len(lines)
        m = len(lines[0])
        alphabet = list(get_alphabet_all(lines))

        return CSProblem(m, n, lines, alphabet)

    def __init__(self, m: int, n: int, strings: List[str], alphabet: List[str]) -> None:
        self.m = m
        self.n = n
        self.strings = strings
        self.alphabet = alphabet

    def __str__(self) -> str:
        lines = []
        lines.append('--CS Problem--')
        lines.append(f'\t{self.n} strings of length {self.m}')
        lines.append(f'\tover finite alphabet of length {len(self.alphabet)}: {self.alphabet}')
        lines.append(f'\tagainst strings:')
        for i, s in enumerate(self.strings):
            lines.append(f'\t\t{i+1}: {s}')
        return '\r\n'.join(lines)


        

class CSSolution:
    def __init__(self, solution: str, measure: int, extra:any = None) -> None:
        self.solution = solution
        self.measure = measure
        self.extra = extra if extra is not None else dict()

    def as_dict(self) -> dict[str, int]:
        return {'solution': self.solution, 'measure': self.measure, 'extra': self.extra}

    def __str__(self) -> str:
        lines = []
        lines.append('--CS Solution--')
        lines.append(f'\tString: {self.solution}')
        lines.append(f'\tScore: {self.measure}')
        lines.append('\tExtra:')
        for e in self.extra:
            lines.append(f'\t\t{e}: {self.extra[e]}')

        return '\r\n'.join(lines)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CSSolution):
            return False
        return self.measure == o.measure



# TODO: Refactor config
class AbstractSolver:
    def __init__(self, **kwargs) -> None:
        self.expected_solution = None
        self.wrong_flag = None
        if 'config' in kwargs:
            self.config = kwargs['config']
        else:
            self.config = self.default_config()
    
    def name(self) -> str:
        raise NotImplementedError

    def default_config(self) -> dict:
        raise NotImplementedError

    def config(self) -> dict:
        if self.config is None:
            return self.default_config()
        return self.config

    def edit_conf(self, k, v):
        self.config[k] = v
        return self

    def read_config(filepath):
        raise NotImplementedError('TODO')

    def solve_(self, problem: CSProblem) -> CSSolution:
        raise NotImplementedError

    def solve(self, problem: CSProblem) -> dict:
        sol = self.solve_(problem)
        if self.expected_solution is not None:
            sol.extra['is_expected'] = sol == self.expected_solution
            sol.extra['expected'] = self.expected_solution.measure
            self.wrong_flag = not sol.extra['is_expected']
        return sol

    def expect(self, solution: CSSolution) -> None:
        self.expected_solution = solution
        return self

    def run_and_time(self, problem: CSProblem) -> dict:
        start_time = time.time()
        solution = self.solve(problem)
        end_time = time.time()

        return {
            'solution': solution,
            'start_time': start_time,
            'end_time': end_time,
            'elapsed': (end_time - start_time)
        }

    

    

    

    

    