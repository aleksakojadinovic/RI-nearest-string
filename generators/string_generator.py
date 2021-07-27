class StringIterator:
    @staticmethod
    def repeat(c, n):
        return ''.join(c for _ in range(n))

    @staticmethod
    def replace_char(s, idx, c):
        return s[:idx] + c + s[idx + 1:]

    def alphabet_index(self, c):
        return self.alphabet.index(c)

    def push_and_kill(self, s):
        curr_char_idx = len(s) - 1
        last_char = self.alphabet[-1]
        while curr_char_idx >= 0 and s[curr_char_idx] == last_char:
            curr_char_idx -= 1
        if curr_char_idx < 0:
            return None

        next_alphabet_letter = self.alphabet[self.alphabet_index(s[curr_char_idx]) + 1]
        return s[:curr_char_idx] + next_alphabet_letter + StringIterator.repeat(self.alphabet[0], self.length - curr_char_idx - 1)
        
    def __init__(self, alphabet, length):
        self.alphabet = list(alphabet)
        self.length = length
        self.current_string = StringIterator.repeat(self.alphabet[0], self.length)

    def __next__(self):
        if self.current_string is None:
            raise StopIteration

        ret = self.current_string
        self.current_string = self.push_and_kill(self.current_string)

        return ret

class StringGenerator:
    def __init__(self, alphabet, length):
        self.alphabet = alphabet
        self.length = length

    def __iter__(self):
        return StringIterator(self.alphabet, self.length)

    