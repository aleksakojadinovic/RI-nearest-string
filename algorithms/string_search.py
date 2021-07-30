import sys
from typing import List
sys.path.append('../')
import utils.utils as ut
from generators.string_generator import StringGenerator
import math

class ystr(str):
    def __or__(self, index_list):
        return ystr(''.join(c for i, c in enumerate(str(self)) if i in index_list))

    def set_char(self, index, char):
        s = str(self)
        return ystr(s[:index] + char + s[index + 1:])

    def diff_idx(self, other):
        return [i for i, (c1, c2) in enumerate(zip(self, other)) if c1 != c2]

    def same_idx(self, other):
        return [i for i, (c1, c2) in enumerate(zip(self, other)) if c1 == c2]

    

def string_search_solver(strings, ds, alphabet):
    m = len(strings[0])
    n = len(strings)
    strings = [ystr(s) for s in strings]
    return string_search_solver_(strings, ds, alphabet, m, n)

def string_search_solver_(strings: List[ystr], ds: List[int], alphabet: List[str], m, n):
    s0 = strings[0]
    i0 = None
    for i in range(n):
        curr_str = strings[i]
        if ut.hamming_distance(s0, curr_str) > ds[i]:
            i0 = i
            break

    if i0 is None:
        return s0

    si0 = strings[i0]
    Q = s0.diff_idx(si0)
    P = [j for j in list(range(0, len(s0))) if j not in Q]

    for t in map(ystr, StringGenerator(alphabet, len(P))):
        if ut.hamming_distance(t, s0 | P) <= ds[0] and ut.hamming_distance(t, si0 | P) <= ds[i0]:
            e1 = min(ds[0] - ut.hamming_distance(t, s0 | P), math.ceil(ds[0] / 2))
            es = [e1] + [ds[i] - ut.hamming_distance(t, strings[i] | P) for i in range(1, len(strings))]
            u = string_search_solver_([s | Q for s in strings], es, alphabet)
            if u is not None:
                final_str = ''
                for i in range(m):
                    if i in P:
                        final_str += t[i]
                    else:
                        final_str += u[i]
                return final_str
    return None
    
    