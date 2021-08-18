import random
import numpy as np
from typing import List
from scipy.optimize import linprog
import utils

def chi(strings, i, j, a):
    if strings[i][j] == a:
        return 0
    return 1

def reconstruct_solution(m, Q, primary_reference_string, x_values, alphabet):
    A = len(alphabet)
    s_prime_as_list = ['' for _ in range(m)]
    p_index = 0
    for x_index in range(m):
        if x_index in Q:
            s_prime_as_list[x_index] = primary_reference_string[x_index]
        else:
            # For each position j we treat all of its a-solutions as the probability distribution
            # for picking the letter a, that is j: (xja1, xja2, ... xja|A|) is the distrib
            candidate_vars = x_values[p_index * A:(p_index + 1) * A]
            # print(f'x_values={x_values}', file=sys.stderr)
            # print(f'candidate vars={candidate_vars}', file=sys.stderr)
            # print(f'Candidate vars sum: {sum(candidate_vars)}')
            alph_idx = random.choices(range(len(candidate_vars)), k=1, weights=candidate_vars)[0]
            s_prime_as_list[x_index] = alphabet[alph_idx]
            p_index += 1

    s_prime = ''.join(s_prime_as_list)
    return s_prime

# Optimize on disagreeing positions
# P - disagreeing positions
# Q - agreeing positions
def solve_by_lp_relaxation(P, Q, alphabet, m, n, original_strings, primary_reference_string):
    LP_T_ = 'float64'

    A = len(alphabet)
    nP = len(P)

    # There are nP*A + 1 variables - nP*A for each xja, and 1 for d
    num_variables = nP*A + 1

    # ======================= CONSTRUCTING THE EQUALITY CONSTRAINTS ========================
    # There are nP constraints with equality
    lp_eq_matrix = np.zeros((nP, num_variables), dtype=LP_T_)
    # For each j we need an "exactly one" constraints
    # The constraint will have ones only within one j-group, and zeros on other positions
    # Therefore we iterate over j-groups
    for i in range(nP):
        left_bound = i*A
        right_bound = (i+1)*A
        lp_eq_matrix[i][left_bound:right_bound] = np.ones(A, dtype=LP_T_)

    # The ds are not in this part and they remain zeros since the matrix was constructed with np.zerps
    # RHS are all ones
    lp_eq_b = np.ones(nP, dtype=LP_T_)

    # ======================= CONSTRUCTING THE INEQUALITY CONSTRAINTS ======================
    # There are n inequality constraints
    # For x_j_a, its absolute position as a variable
    # is j*A + a
    lp_leq_matrix = np.zeros((n, num_variables), dtype=LP_T_)
    # Each of them has -1 coefficient with d, and those correspond to the very last column
    lp_leq_matrix[:, -1] = -np.ones(n, dtype=LP_T_)
    # Other coefficients are chi(i, j, a)
    for i in range(n):
        for a in range(A):
            for j in range(nP):
                actual_var_idx = j*A + a
                lp_leq_matrix[i][actual_var_idx] = chi(original_strings, i, j, alphabet[a])
    # RHS are -d(si|Q, s'|Q)
    lp_leq_b = -np.array([utils.hamming_distance(utils.sat(original_strings[i], Q), utils.sat(primary_reference_string, Q)) for i in range(n)], dtype='int32')

    # Target function is just 'd'
    c = np.zeros(num_variables, dtype=LP_T_)
    c[-1] = 1

    # Every variable must be positive
    lower_bounds = [0.0 for _ in range(num_variables)]
    # xs are constrainted by 1, d is unconstrained above
    upper_bounds: List[any] = [1.0 for _ in range(num_variables-1)] + [None]


    # Now we just plug it into scipy's solver
    # sout, serr = sys.stdout, sys.stderr
    # sys.stdout, sys.stderr = None, None
    lp_solution = linprog(c,
                          A_ub=lp_leq_matrix,
                          b_ub=lp_leq_b,
                          A_eq=lp_eq_matrix,
                          b_eq=lp_eq_b,
                          bounds=list(zip(lower_bounds, upper_bounds)))
    # sys.stdout, sys.stderr = sout, serr


    if not lp_solution.success:
        print('not stonks')
        return None

    # print(lp_solution)
    s_prime = reconstruct_solution(m, Q, primary_reference_string, lp_solution.x, alphabet)
    return s_prime, utils.problem_metric(s_prime, original_strings)
