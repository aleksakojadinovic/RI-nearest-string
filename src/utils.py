def sat(s, I):
    return ''.join(c for i, c in enumerate(s) if i in I)

def Q(s1, s2):
    return [i for i, (c1, c2) in enumerate(zip(s1, s2)) if c1 == c2]

def P(s1, s2):
    return [i for i, (c1, c2) in enumerate(zip(s1, s2)) if c1 != c2]

def Q_all(strings):
    if not strings:
        return []
    ref = strings[0]
    return [i for i in range(len(ref)) if all((s[i] == ref[i] for s in strings))]



def hamming_distance(s1, s2):
    return sum(c1 != c2 for c1, c2 in zip(s1, s2))

def hamming_at(s1, s2, I):
    h = 0
    for i in I:
        if s1[i] != s2[i]:
            h += 1
    return h

def problem_metric(string, references):
    return max(hamming_distance(string, r) for r in references)

def problem_metric_at(string, references, I):
    return max(hamming_at(string, r, I) for r in references)

# Returns the alphabet for a given string
def get_alphabet(s):
    return set(list(s))

# Returns the alphabet for a given list of strings
def get_alphabet_all(strings):
    alphabet = set()
    for s in strings:
        alphabet = alphabet.union(get_alphabet(s))
    return alphabet






