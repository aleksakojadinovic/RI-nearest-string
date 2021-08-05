import random
import sys
sys.path.append('../utils')
sys.path.append('../generators')
import utils.utils as ut
from generators import random_generator
from .abstractions import *
from tqdm import tqdm

class PSOSolver(AbstractSolver):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def default_config(self) -> dict:
        return {
            'PARTICLES': 1000,
            'MAX_ITERS': 10000,
            'LR': 0.7
        }

    def solve_(self, problem: CSProblem) -> CSSolution:
        
        return None