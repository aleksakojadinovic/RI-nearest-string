import sys
from tqdm import tqdm
from typing import List

from numpy import euler_gamma
sys.path.append('../solvers')
from solvers.abstractions import *

import matplotlib.pyplot as plt


def compare_on_single_problem(solvers: List[AbstractSolver], problem: CSProblem, ax = None):
    if ax is None:
        ax = plt
    
    results = []
    for s in solvers:
        print(f'Running solver: {s.name()}')
        results.append(s.run_and_time(problem))
    times = [r['elapsed'] for r in results]
    names = [s.name() for s in solvers]

    ax.bar(range(len(solvers)), times, align='center')
    ax.xticks(range(len(solvers)), names)
    ax.ylabel('Time (seconds)')
    ax.title('Comparing different solvers')


def compare_on_range_of_problems(solvers: List[AbstractSolver], problems: List[CSProblem], target_var_range: List, target_var_name: str, ax = None):
    if ax is None:
        ax = plt
    if len(problems) != len(target_var_range):
        print(f'Target var range must have the same number of elements as problems')
    solvers_times = []
    for solver in solvers:
        print(f'Solver {solver.name()}')
        this_solver_times = []
        for problem in tqdm(problems):
            res = solver.run_and_time(problem)
            this_solver_times.append(res['elapsed'])
        solvers_times.append(this_solver_times)

    for solver, solver_times in zip(solvers, solvers_times):
        ax.plot(target_var_range, solver_times, label=solver.name())
        
    ax.xlabel(target_var_name)
    ax.ylabel('Time (in seconds)')
    ax.legend()
    
    


