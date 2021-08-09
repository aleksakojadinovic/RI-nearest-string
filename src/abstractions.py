import time

import utils as ut
from typing import List


class CSProblem:
    @staticmethod
    def from_dict(d):
        return CSProblem(d['m'], d['n'], d['strings'], d['alphabet'], d['expect'])

    @staticmethod
    def from_csp(filepath):
        f = open(filepath, 'r')
        lines = f.read().splitlines()
        lines = (l for l in lines if l)
        lines = list(lines)

        alphabet_size = int(lines[0])
        n = int(lines[1])
        m = int(lines[2])
        alphabet = lines[3:3+alphabet_size]
        strings = lines[3+alphabet_size:]

        return CSProblem(m, n, strings, alphabet)

    @staticmethod
    def from_file(filepath):

        f = open(filepath, 'r')
        lines = f.read().splitlines()
        lines = (l for l in lines if not l.startswith('#'))
        lines = (l for l in lines if l)
        lines = list(lines)
        if not lines:
            raise ValueError(f'Empty file.')
        try:
            n = int(lines[0])
        except ValueError:
            raise ValueError(f'Expected number of strings in the first line, got {lines[0]}')
        # Now we need either n more lines of n + 1 more lines
        # if there are n lines then they're all strings
        expected_solution = None
        string_entries = []
        if len(lines) == n + 1:
            string_entries = lines[1:]
        elif len(lines) == n + 2:
            if lines[-1].lower().startswith('expect'):
                expect_entry = lines[-1].split(" ")
            else:
                raise ValueError(f'Unknown command: {lines[-1]} (maybe number of strings is wrong?)')
            if len(expect_entry) != 2:
                raise ValueError(f'Invalid expect syntax, should be "expect SOLUTION"!')
            d_str = expect_entry[1]
            try:
                d_num = int(d_str)
            except ValueError:
                raise ValueError('Non-integer in expect syntax!')

            if d_num < 0:
                raise ValueError(f'Expected value cannot be negative!')

            expected_solution = d_num
            string_entries = lines[1:][:-1]
        else:
            raise ValueError(f'Unexpected number of lines')

        m = len(string_entries[0])
        if not all(len(s) == m for s in string_entries):
            raise ValueError(f'Strings need to be of same size!')
        alphabet = list(ut.get_alphabet_all(string_entries))

        return CSProblem(m, n, string_entries, alphabet, expect=expected_solution)

    def __init__(self, m: int, n: int, strings: List[str], alphabet: List[str], expect: int = None) -> None:
        self.m = m
        self.n = n
        self.strings = strings
        self.alphabet = alphabet
        self.expect = expect

    def __str__(self) -> str:
        lines = []
        lines.append('--CS Problem--')
        lines.append(f'\t{self.n} strings of length {self.m}')
        lines.append(f'\tover finite alphabet of length {len(self.alphabet)}: {self.alphabet}')
        lines.append(f'\tagainst strings:')
        for i, s in enumerate(self.strings):
            lines.append(f'\t\t{i + 1}: {s}')
        if self.expect is not None:
            lines.append(f'\tExpecting solution: {self.expect}')
        return '\r\n'.join(lines)


class CSSolution:
    def __init__(self, solution: str, measure: int, extra: any = None, problem: CSProblem = None) -> None:
        self.solution = solution
        self.measure = measure
        self.extra = extra if extra is not None else dict()
        self.problem = problem
        if problem is None or problem.expect is None:
            self.correct = None
        else:
            self.correct = self.measure == problem.expect

    def as_dict(self) -> dict[str, int]:
        return {'solution': self.solution, 'measure': self.measure, 'extra': self.extra, 'correct': self.correct}

    def compare_with_ref_(self, expected_value):
        self.correct = expected_value == self.measure

    def __str__(self) -> str:
        lines = []
        lines.append('--CS Solution--')
        lines.append(f'\tString: {self.solution}')
        lines.append(f'\tScore: {self.measure}')
        lines.append('\tExtra:')
        for e in self.extra:
            lines.append(f'\t\t{e}: {self.extra[e]}')
        lines.append(f'Correct: {self.correct if self.correct is not None else "Unknown"}')

        return '\r\n'.join(lines)

    def __eq__(self, o: object) -> bool:
        if not isinstance(o, CSSolution):
            return False
        return self.measure == o.measure


class AbstractSolver:
    def __init__(self, **kwargs) -> None:
        if 'config' in kwargs:
            self.config = kwargs['config']
        else:
            self.config = self.get_default_config()

    def name(self) -> str:
        raise NotImplementedError

    def get_default_config(self) -> dict:
        raise NotImplementedError

    def get_config(self) -> dict:
        return self.config

    def edit_conf(self, k, v):
        self.config[k] = v
        return self

    def solve_(self, problem: CSProblem) -> CSSolution:
        raise NotImplementedError

    def solve(self, problem: CSProblem) -> CSSolution:
        sol = self.solve_(problem)
        if problem.expect is not None:
            sol.compare_with_ref_(problem.expect)
        return sol

    def run_and_time(self, problem: CSProblem) -> dict:
        start_time = time.time()
        solution = self.solve_(problem)
        end_time = time.time()

        if problem.expect is not None:
            solution.compare_with_ref_(problem.expect)

        return {
            'solution': solution,
            'start_time': start_time,
            'end_time': end_time,
            'elapsed': (end_time - start_time)
        }


