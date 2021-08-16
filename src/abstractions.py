import time
import os
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

    def save_to_file(self, filepath):
        lines = []
        lines.append(str(self.n))
        lines += [s for s in self.strings]
        if self.expect is not None:
            lines.append(f'expect {self.expect}')
        f = open(filepath, 'w')
        f.write("\n".join(lines))


class CSPLoader:
    def __init__(self, solution_file=None):
        self.solutions = dict()
        if solution_file is not None:
            f = open(solution_file, 'r')
            lines = f.read().splitlines()
            lines = (l for l in lines if l)
            lines = list(lines)[1:]
            for line in lines:
                # print(f'line: {line}')

                first_sc_index = line.index(';')
                if first_sc_index == -1:
                    continue
                second_sc_index = line[first_sc_index+1:].index(';')

                if second_sc_index == -1:
                    continue
                second_sc_index += first_sc_index + 1

                problem_name = line[:first_sc_index]
                # print(f'problem name: {problem_name}')
                # print(f'problem_sol_string: {line[first_sc_index+1:second_sc_index]}')
                # print(f'first sc index: {first_sc_index}')
                # print(f'second sc index: {second_sc_index}')
                #
                # print(f'indexing string {line} from {first_sc_index+1} to {second_sc_index} results in {line[first_sc_index+1:second_sc_index]}')

                problem_solution = float(line[first_sc_index+1:second_sc_index])
                self.solutions[problem_name] = problem_solution



    def load_csp(self, filepath):
        fname = os.path.basename(filepath)
        problem = CSProblem.from_csp(filepath)
        problem.expect = None if fname not in self.solutions else self.solutions[fname]
        return problem





class CSSolution:
    def __init__(self, solution: str, measure: int, problem: CSProblem, extra: any = None) -> None:
        self.solution = solution
        self.measure = measure
        self.extra = extra if extra is not None else dict()
        self.problem = problem
        self.quality = (problem.m - self.measure) / problem.m
        self.objective_quality = None


    def compare_with_ref_(self, expected_value):
        self.objective_quality = expected_value / self.measure

    def __str__(self) -> str:
        lines = []
        lines.append('--CS Solution--')
        lines.append(f'\tString: {self.solution}')
        lines.append(f'\tScore: {self.measure}')
        lines.append(f'\tQuality: {self.quality}')
        lines.append(f'\tObjective quality: {self.objective_quality}')
        lines.append('\tExtra:')
        for e in self.extra:
            lines.append(f'\t\t{e}: {self.extra[e]}')


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
        solution = self.solve(problem)
        end_time = time.time()

        if problem.expect is not None:
            solution.compare_with_ref_(problem.expect)

        return {
            'solution': solution,
            'start_time': start_time,
            'end_time': end_time,
            'elapsed': (end_time - start_time)
        }


