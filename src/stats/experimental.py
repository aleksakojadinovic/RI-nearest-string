import json
import sys
import os
import pandas as pd
from tqdm import tqdm
import generators.random_generator
from typing import List
from abstractions import AbstractSolver, CSProblem
from statistics import stdev, mean

DEFAULT_TRIALS_PER_PROBLEM = 5

standard_col_names = ['Average running time',
                      'Running time stdev',
                      'Average score',
                      'Score stdev',
                      'Average quality',
                      'Average objective quality'
                      ]

class Benchmarker:

    @staticmethod
    def test_solver_against_problems(solver: AbstractSolver,
                                      packet,
                                      trials_per_problem=DEFAULT_TRIALS_PER_PROBLEM,
                                      out_format='pandas'):
        results = []
        problem_list, param_range, param_name = packet['problem_list'], packet['target_param_range'], packet['target_param_name']

        for i, p in tqdm(list(enumerate(problem_list))):
            p_results = [solver.run_and_time(p) for _ in range(trials_per_problem)]
            p_times  =  [res.elapsed for res in p_results]
            p_scores =  [res.measure for res in p_results]
            p_qualities = [res.quality for res in p_results]
            p_objective_qualities = [res.objective_quality for res in p_results]

            p_avg_time  = mean(p_times)
            p_avg_score = mean(p_scores)
            p_avg_quality = 100.0 * mean(p_qualities)
            p_avg_objective_quality = 100* mean(p_objective_qualities) if p.expect is not None else None
            p_time_stdev = stdev(p_times) if trials_per_problem >= 2 else None
            p_score_stdev = stdev(p_scores) if trials_per_problem >= 2 else None


            entry_idx = param_range[i] if param_range is not None else i
            entry = [entry_idx, p_avg_time, p_time_stdev, p_avg_score, p_score_stdev, p_avg_quality, p_avg_objective_quality]
            results.append(entry)

        if out_format == 'pandas':
            param_n = param_name if param_name is not None else 'Test parameter'
            df = pd.DataFrame(results, columns=[param_n] + standard_col_names)
            return df

        return results

    @staticmethod
    def get_benchmark_packet(other_params, target_param_range, target_param_name):
        try:
            if 'alphabet' not in other_params:
                # Meaning alphabet size is the varying parameter
                problem_list = generators.random_generator.random_problems_over_alph_size(target_param_range,
                                                                                          other_params['n'],
                                                                                          other_params['m'])
            elif 'm' not in other_params:
                problem_list = generators.random_generator.random_problems_over_string_size(target_param_range,
                                                                                            other_params['alphabet'],
                                                                                            other_params['n'])
            elif 'n' not in other_params:
                problem_list = generators.random_generator.random_problems_over_num_of_strings(target_param_range,
                                                                                               other_params['alphabet'],
                                                                                               other_params['m'])
            else:
                raise ValueError(f'All params provided.')
        except KeyError:
            raise ValueError(f'Insufficient number of other params.')

        return {
            'problem_list': problem_list,
            'target_param_name': target_param_name,
            'target_param_range': target_param_range
        }


    @staticmethod
    def save_benchmark_packet(packet, parent_directory, packet_name=None, packet_name_prefix=None):
        problem_list,\
        target_param_name,\
        target_param_range = packet['problem_list'],\
                             packet['target_param_name'],\
                             list(packet['target_param_range'])

        if packet_name is None:
            prefix = '' if packet_name_prefix is None else packet_name_prefix + '_'
            packet_name = f'{prefix}bp_{target_param_name}_{target_param_range[0]}-{target_param_range[-1]}'

        if parent_directory not in filter(os.path.isdir, os.listdir(os.getcwd())):
            os.mkdir(parent_directory)

        os.makedirs(f'{parent_directory}/{packet_name}')
        for i, p in enumerate(problem_list):
            problem_marker = target_param_range[i]
            problem_name = f'{problem_marker}.txt'
            p.save_to_file(f'{parent_directory}/{packet_name}/{problem_name}')

        other = {'target_param_name': target_param_name,
                 'target_param_range': target_param_range}

        json.dump(other, open(f'{parent_directory}/{packet_name}/_packet_info.json', 'w'))

    @staticmethod
    def load_benchmark_packet(dirpath):
        if '_packet_info.json' not in os.listdir(dirpath):
            raise ValueError(f'Packet info file missing.')

        packet = json.load(open(f'{dirpath}/_packet_info.json', 'r'))


        problem_files = [fname for fname in os.listdir(dirpath) if fname != '_packet_info.json']
        # May the lord forgive me for what I'm about to do
        problem_files.sort(key=lambda fname: int(fname[:fname.index(".")]))
        problem_list = [CSProblem.from_file(f'{dirpath}/{fname}') for fname in problem_files]




        packet['problem_list'] = problem_list
        return packet
















