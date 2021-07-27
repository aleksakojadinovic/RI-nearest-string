import sys
sys.path.append('../')
import utils.utils as ut
from generators.string_generator import StringGenerator
import math

def diff_index_list(s1, s2):
    l = []
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2:
            l.append(i)
    return l

def yank(s, P):
    return ''.join(c for i, c in enumerate(s) if i in P)

def string_search_solver_(strings, ds, alphabet):
    m = len(strings[0])
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
    Q = diff_index_list(s0, si0)
    P = [j for j in list(range(0, len(s0))) if j not in Q]

    for t in StringGenerator(alphabet, len(P)):
        if ut.hamming_distance(t, yank(s0, P)) <= ds[0] and ut.hamming_distance(t, yank(si0, P)) <= ds[i0]:
            e1 = min(ds[0] - ut.hamming_distance(t, yank(s0, P)), math.ceil(ds[0] / 2))
            es = [e1] + [ds[i] - ut.hamming_distance(t, yank(strings[i], P)) for i in range(1, len(strings))]
            u = string_search_solver_([yank(s, Q) for s in strings], es, alphabet)
            if u is not None:
                final_str = ''
                for i in range(m):
                    if i in P:
                        final_str += t[i]
                    else:
                        final_str += u[i]
                return final_str
    return None
    
    