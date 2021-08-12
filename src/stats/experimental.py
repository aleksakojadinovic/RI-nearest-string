import pandas as pd
import sys

from tqdm import tqdm

import generators.random_generator

from typing import List
from abstractions import AbstractSolver, CSProblem
from statistics import stdev

DEFAULT_TRIALS_PER_PROBLEM = 5

standard_col_names = ['Average running time',
                      'Running time stdev',
                      'Average score',
                      'Score stdev',
                      'Average quality',
                      'Objective quality'
                      ]

class Benchmarker:

    @staticmethod
    def test_solver_against_problems_(solver: AbstractSolver,
                                      problem_list: List[CSProblem],
                                      trials_per_problem=DEFAULT_TRIALS_PER_PROBLEM,
                                      index=None,
                                      out_format='pandas'):
        results = []
        for p in tqdm(problem_list):
            p_results = [solver.run_and_time(p) for _ in range(trials_per_problem)]
            p_times  =  [res["elapsed"] for res in p_results]
            p_scores =  [res["solution"].measure for res in p_results]


            p_avg_time  = sum(p_times) / trials_per_problem
            p_avg_score = sum(p_scores) / trials_per_problem
            p_avg_quality = 100.0 * (p.m - p_avg_score) / p.m
            p_objective_quality = None if p.expect is None else 100.0*p.expect / p_avg_score
            p_time_stdev = stdev(p_times) if trials_per_problem >= 2 else None
            p_score_stdev = stdev(p_scores) if trials_per_problem >= 2 else None

            results.append([p_avg_time, p_time_stdev, p_avg_score, p_score_stdev, p_avg_quality, p_objective_quality])

        if out_format == 'pandas':
            df = pd.DataFrame(results, columns=standard_col_names)
            if index is not None:
                df.index = index
            return df

        return results

    @staticmethod
    def test_solver_against_problems(solver: AbstractSolver,
                                     target_param_range,
                                     other_params,
                                     target_param_name='Target parameter',
                                     trials_per_problem=DEFAULT_TRIALS_PER_PROBLEM):
        # Check which parameters are there and which are not
        try:
            if 'alphabet' not in other_params:
                # Meaning alphabet size is the varying parameter
                problem_list = generators.random_generator.random_problems_over_alph_size(target_param_range, other_params['n'], other_params['m'])
            elif 'm' not in other_params:
                problem_list = generators.random_generator.random_problems_over_string_size(target_param_range, other_params['alphabet'], other_params['n'])
            elif 'n' not in other_params:
                problem_list = generators.random_generator.random_problems_over_num_of_strings(target_param_range, other_params['alphabet'], other_params['m'])
            else:
                raise ValueError(f'All params provided.')
        except KeyError:
            raise ValueError(f'Insufficient number of other params.')


        results = Benchmarker.test_solver_against_problems_(solver, problem_list, trials_per_problem, index=list(target_param_range))

        return results







