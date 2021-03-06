import sys
sys.path.append('../utils')
import utils.utils as ut
import random
import string
import time

def random_alphabet(length):
    alph = set()
    while True:
        if len(alph) == length:
            break
        letter = random.choice(string.ascii_letters)
        alph.add(letter)

    return list(alph)

def random_string(alphabet, length):
    s = str.join('', [random.choice(alphabet) for _ in range(length)])
    return s

def random_strings(n, alphabet, length):
    ss = [random_string(alphabet, length) for _ in range(n)]
    return ss

def random_problem(n, alphabet_length, string_length):
    a = random_alphabet(alphabet_length)
    strings = random_strings(n, a, string_length)
    return {
        'n': n,
        'm': string_length,
        'strings': strings,
        'alphabet': a
    }

def random_problems_over_alph_size(max_alphabet_size, n, string_length):
    return [random_problem(n, i, string_length) for i in range(1, max_alphabet_size + 1)]







    
