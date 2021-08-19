import random
import string

import utils
from abstractions import CSProblem

alphabet_choice_set = list(set(list(string.ascii_letters) + [str(i) for i in range(10)] + list('!@#$%^&*()-=_+[]{};"\\:|,./<>/')))

def random_alphabet(length):
    alph = set()
    while True:
        if len(alph) == length:
            break
        letter = random.choice(alphabet_choice_set)
        if letter in alph:
            continue
        alph.add(letter)

    return list(alph)

def random_string(alphabet, m):
    s = ''.join(random.choice(alphabet) for _ in range(m))
    return s

def random_strings(n, alphabet, m):
    ss = [random_string(alphabet, m) for _ in range(n)]
    return ss

def random_problem(n, alphabet, m):
    strings = random_strings(n, alphabet, m)
    return CSProblem(m, n, strings, alphabet)


# TODO: this doesnt work now
def random_problems_over_alph_size(alph_range, n, m):
    ps = []
    for a_size in alph_range:
        alphabet = random_alphabet(a_size)
        strings = random_strings(n, alphabet, m)
        ps.append(CSProblem(m, n, strings, alphabet))
    return ps



def random_problems_over_string_size(m_range, alphabet, n):
    ps = []
    for m in m_range:
        strs = random_strings(n, alphabet, m)
        p = CSProblem(m, n, strs, alphabet)
        ps.append(p)

    return ps

def random_problems_over_num_of_strings(n_range, alphabet, m):
    ps = []
    for n in n_range:
        strs = random_strings(n, alphabet, m)
        p = CSProblem(m, n, strs, alphabet)
        ps.append(p)

    return ps

def random_not_(coll, a):
    if len(coll) == 1 and coll[0] == a:
        raise ValueError(f'This pick is impossible.')
    while True:
        pick = random.choice(coll)
        if pick != a:
            return pick

def truly_modify_at_(s, position, alphabet):
    nc = random_not_(alphabet, s[position])
    return s[:position] + nc + s[position+1:]

def truly_modify_at_idxs(s, positions, alphabet):
    for p in positions:
        s = truly_modify_at_(s, p, alphabet)
    return s

def truly_modify_at_random_positions(s, alphabet, n_pos):
    if n_pos == 0:
        return s
    idxs = random.sample(range(len(s)), k=n_pos)
    # print(idxs)
    return truly_modify_at_idxs(s, idxs, alphabet)


def generate_solvable_problem(m, n, alphabet, target_solution):
    # Generating a problem backwards, such that
    # max(h(s, si)) = target solution, which we will treat as

    if target_solution < 0 or target_solution > m:
        raise ValueError(f'Invalid target solution value.')


    solution_string = random_string(alphabet, m)
    # Now we need to construct n strings such that
    # they differ from solution_string at up to target_solution characters
    # Keep in mind that at least one string must be at exactly target_solution characters,
    # otherwise the target_solution is not actually optimal
    # So we will say that a random number of strings between (1, n) will take that value
    orig_fake_string = truly_modify_at_random_positions(solution_string, alphabet, target_solution)
    strings = [orig_fake_string]

    for i in range(1, n):
        new_str = truly_modify_at_random_positions(solution_string, alphabet, random.randint(0, target_solution))
        strings.append(new_str)

    random.shuffle(strings)

    wsm = utils.problem_metric(solution_string, strings)
    if wsm != target_solution:
        print(f'Failed....')

    # assertion step


    return CSProblem(m, n, strings, alphabet, expect=target_solution)







    pass

