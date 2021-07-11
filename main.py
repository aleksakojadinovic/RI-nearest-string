import utils.utils as ut
from solvers.brute_force_search import brute_force_dfs
from solvers.pruning_search import pruning_dfs
import sys
import time
import datetime
if __name__ == '__main__':
    input_file = 'examples/ex1.txt'
    problem = ut.read_from_file(input_file)
    

    if sys.argv[1] == 'brute':    
        res = ut.run_and_time(brute_force_dfs, problem)
    else:
        res = ut.run_and_time(pruning_dfs, problem)


    print(f'Success: {res["success"]}')
    print(f'Result:  {res["best_string"]}')
    print(f'Score:   {res["best_score"]}')
    print( 'Time:    {:.3f}s'.format(res["time"]))





