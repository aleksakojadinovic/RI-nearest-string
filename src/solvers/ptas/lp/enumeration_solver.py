# Optimize on P positions
# in reference to the original strings
# keeping other values fixed to that of primary_reference_string
def replace(s, i, c):
    return s[:i] + c + s[i+1:]


def partial_hamming_at_(s1, s2, I, upto):
    h = 0
    for i in I[:upto]:
        if s1[i] != s2[i]:
            h += 1

    return h

def partial_metric_at(s, references, I, upto):
    return max(partial_hamming_at_(s, r, I, upto) for r in references)



def solve_by_force(P, Q, alphabet, m, n, original_strings, primary_reference_string):
    nP = len(P)

    best_score = nP
    best_string = None
    q = [(primary_reference_string, 0)]
    print(f'Starting force search')
    print(f'\t WCS leaves {len(alphabet)} ^ {nP}: {len(alphabet)**nP}')
    while q:
        curr_string, curr_p_idx = q.pop()
        curr_string_metric = partial_metric_at(curr_string, original_strings, P, curr_p_idx)
        if curr_string_metric >= best_score:
            continue

        if curr_p_idx == nP:
            if curr_string_metric <= best_score:
                best_score = curr_string_metric
                best_string = curr_string
            continue

        q += [(replace(curr_string, P[curr_p_idx], a), curr_p_idx + 1) for a in alphabet]


    return best_string, best_score