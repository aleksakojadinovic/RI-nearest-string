class IntegerProgrammingBBSolver:

    def __init__(self,
                 c,
                 A_leq, b_leq,
                 A_eq, b_eq):
        self.c = c
        self.A_leq = A_leq
        self.b_leq = b_leq
        self.A_eq = A_eq
        self.b_eq = b_eq

