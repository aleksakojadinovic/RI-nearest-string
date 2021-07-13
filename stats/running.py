import time
import sys
sys.path.append('../generators')
from generators.random_generator import random_problem

def run_and_time(solver, problem):
    start_time = time.time()
    res = solver(problem)
    end_time = time.time()
    elapsed = end_time - start_time
    res['time'] = elapsed
    return res

def simulate_random_over_alphabet_size(solvers, max_alphabet_size, n, m):
    problems = [random_problem(n, i, m) for i in range(1, max_alphabet_size + 1)]
    times = []
    for s in solvers:
        
        c_times = []
        for i, p in enumerate(problems):
            print(f'Running solvers for problem {i+1}/{len(problems)}', end='\r')
            c_times.append(run_and_time(s, p)['time'])
        times.append(c_times)
        print(f'')
        print(f'')

    
    print(f'Done!')
    return times