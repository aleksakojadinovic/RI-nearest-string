import sys
sys.path.append('../utils')
import utils.utils as ut

def string_search_solver_(strings, ds):
    s0 = strings[0]
    i0 = None
    for i in range(len(strings)):
        curr_str = strings[i]
        if ut.hamming_distance(s0, curr_str) > ds[i]:
            i0 = i
            break

    if i0 is None:
        return s0

    si0 = strings[i0]
    Q = ut.diff_index_list(s0, si0)
    P = [j for j in list(range(0, len(s0))) if j not in Q]
    
    