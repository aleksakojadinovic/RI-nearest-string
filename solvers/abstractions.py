class AbstractSoler:
    @staticmethod
    def from_dict(problem_dict):
        raise NotImplementedError

    def from_file(filepath):
        raise NotImplementedError

    def __init__(self, m, n, strings) -> None:
        self.m = m
        self.n = n
        self.strings = strings

    

    

    