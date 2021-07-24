import random
import sys
sys.path.append('../utils')
sys.path.append('../generators')
import utils.utils as ut
from generators import random_generator

POP_SIZE    = 1000
MAX_ITERS   = 100
TOUR_SIZE   = 10
REPR_SIZE   = 300
MUT         = 0.05


def init_pop(pop_size, alphabet, length):
    return random_generator.random_strings(pop_size, alphabet, length)

def tournament_selection(pop, scores):
    entries = zip(pop, scores)
    selected = random.sample(list(entries), TOUR_SIZE)

    (winner, score) = min(selected, key = lambda x: x[1])
    return winner, score

def perform_selection(pop, scores):
    for_reproduction = [tournament_selection(pop, scores) for _ in range(REPR_SIZE)]
    return for_reproduction
    

def get_best(pop, scores):
    best_unit = None
    best_score = None
    for p, s in zip(pop, scores):
        if best_unit is None or s < best_score:
            best_score = s
            best_unit = p
    return best_unit, best_score

def crossover(s1, s2):
    break_point = random.randrange(1, len(s1))
    return s1[:break_point] + s2[break_point:]

def mutate(s, alphabet):
    random_value = random.random()
    
    if random_value < MUT:

        random_index = random.randrange(len(s))
        
        while True:
            new_value = random.choice(alphabet)
            if s[random_index] != new_value:
                break
                
        s = s[:random_index] + new_value + s[random_index + 1:]
        
    return s
        


def reproduce(for_reproduction, strings, alphabet):
    new_gen = []
    new_gen_scores = []
    while len(new_gen) != POP_SIZE:
        [(parent1, _), (parent2, _)] = random.sample(for_reproduction, 2)
        new_string = crossover(parent1, parent2)
        new_string = mutate(new_string, alphabet)
        new_string_score = ut.problem_metric(new_string, strings)

        new_gen.append(new_string)
        new_gen_scores.append(new_string_score)
    return new_gen, new_gen_scores

    
def genetic_solver(problem_input):
    m = problem_input['m']
    alphabet = problem_input['alphabet']
    strings = problem_input['strings']
    n = len(strings[0])

    current_pop     = init_pop(POP_SIZE, alphabet, n)
    current_scores  = [ut.problem_metric(s, strings) for s in current_pop]
    best_unit, best_score = get_best(current_pop, current_scores)

    score_history = []
    for i in range(MAX_ITERS):
        for_reproduction = perform_selection(current_pop, current_scores)
        new_pop, new_pop_score = reproduce(for_reproduction, strings, alphabet)
        curr_best, curr_best_score = get_best(new_pop, new_pop_score)
        score_history.append(curr_best_score)
        print(f'Iter: {i}/{MAX_ITERS}, score: {curr_best_score}', end='\r')
        if curr_best_score < best_score:
            best_unit = curr_best
            best_score = curr_best_score

    print(f'Best string: {best_unit} with score {best_score}')
    print(score_history)


    
    

    

