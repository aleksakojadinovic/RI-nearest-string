import sys
sys.path.append('../utils')
import utils.utils as ut
import random
import string


def random_alphabet(length):
    return [random.choice(string.ascii_letters) for _ in range(length)]

def random_string(alphabet, length):
    return str.join('', [random.choice(alphabet) for _ in range(length)])

def random_strings(n, alphabet, length):
    return [random_string(alphabet, length) for _ in range(n)]




    
