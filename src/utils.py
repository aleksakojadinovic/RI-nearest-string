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

def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def hamming_distance_is(s1, s2, P):
    return sum(s1[i] != s2[i] for i in P)

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






