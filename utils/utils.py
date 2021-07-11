import time

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def problem_metric(string, references):
    return max(hamming_distance(string, r) for r in references)

# Returns the alphabet for a given string
def get_alphabet(s):
    return set(list(s))

# Returns the alphabet for a given list of strings
def get_alphabet_all(strings):
    alphabet = set()
    for s in strings:
        alphabet = alphabet.union(get_alphabet(s))
    return alphabet

def parse_problem(input_strings):
    input_strings = list(set(input_strings))
    n = len(input_strings)    
    if n == 0:
        raise ValueError('The list has 0 elements.')
    m = len(input_strings[0])
    if not all(len(s) == m for s in input_strings):
        raise ValueError('Expecting strings of equal lengths.')
    
    alphabet = list(get_alphabet_all(input_strings))
    
    return {'n': n, 'm': m, 'strings': input_strings, 'alphabet': alphabet}

def read_from_file(filepath):
    f = open(filepath, 'r')
    lines = f.read().splitlines()
    return parse_problem(lines)

def print_problem(problem_input):
    print('>> Nearest String problem for: ')
    print(f"\t{problem_input['n']} strings of length {problem_input['m']}")
    print(f"\tOver finite alphabet: {problem_input['alphabet']}")
    print(f"\tStrings: ")
    print("\t" + "\n\t".join(problem_input['strings']))


def run_and_time(solver, problem):
    start_time = time.time()
    res = solver(problem)
    end_time = time.time()
    elapsed = end_time - start_time
    res['time'] = elapsed
    return res
    

