import sys
sys.path.append('../utils')
import utils.utils as ut

def brute_force_dfs(problem_input):
    m = problem_input['m']
    alphabet = problem_input['alphabet']
    strings = problem_input['strings']

    q = ['']
    min_hamming = float('inf')
    min_string = None

    iterations = 0
    while q:
        iterations += 1
        curr_string = q.pop()
        curr_string_length = len(curr_string)
        if curr_string_length == m:
            curr_string_score = ut.problem_metric(curr_string, strings)
            if curr_string_score < min_hamming:
                min_hamming = curr_string_score
                min_string = curr_string
            continue
        q += [curr_string + next_letter for next_letter in alphabet]

    return {
        "success": True,
        "best_string": min_string,
        "best_score": min_hamming
        }