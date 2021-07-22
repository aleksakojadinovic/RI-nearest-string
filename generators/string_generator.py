def replace_char(s, idx, c):
    return s[:idx] + c + s[idx + 1:]

class StringIterator:
    def __init__(self, alphabet, length):
        self.alphabet = list(alphabet)
        self.length = length
        self.current_string = ''.join(self.alphabet[0] for _ in range(self.length))
        self.curr_character_index = self.length - 1
        self.curr_alphabet_index = 0
        self.stop = False

    def __next__(self):
        if self.stop:
            raise StopIteration

        ret = self.current_string

        self.curr_alphabet_index += 1
        if self.curr_alphabet_index == len(self.alphabet):
            self.curr_alphabet_index = 0
            self.curr_character_index -= 1
        
        if self.curr_character_index < 0:
            self.stop = True

        self.current_string = replace_char(self.current_string, self.curr_character_index, self.alphabet[self.curr_alphabet_index])
        return ret

class StringGenerator:
    def __init__(self, alphabet, length):
        self.alphabet = alphabet
        self.length = length

    def __iter__(self):
        return StringIterator(self.alphabet, self.length)

    