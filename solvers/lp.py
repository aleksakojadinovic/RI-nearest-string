import sys
sys.path.append('../utils')
import utils.utils as ut
import numpy as np

from scipy.optimize import linprog

def to_lp_problem(problem):
    m = problem['m']
    n = problem['n']
    constraint_matrix = np.zeros((n, m*n+1))
    for i in range(n):
        constraint_matrix[i, i*m:(i+1)*m] = np.ones(m)
        constraint_matrix[i, -1] = -1
    b_vector = np.zeros(n)
    target_function = np.zeros(m*n+1)
    target_function[-1] = 1
    return constraint_matrix, b_vector, target_function

def solve_as_lp(problem):
    A, b, c = to_lp_problem(problem)

    solution = linprog(c, A_ub=A, b_ub=b)

    print(solution)

        
    