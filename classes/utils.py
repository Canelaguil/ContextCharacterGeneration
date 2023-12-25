import numpy as np
from numpy import random
from random import choices as weighted_choice
import sys 

"""
MODIFIERS
"""
def fair_mod(value, mod, high=1, round_dec=3):
    """
    Modify value fairly using fair math: 
    https://choicescriptdev.fandom.com/wiki/Arithmetic_operators#Fairmath
    """
    if mod > 0:
        value = value + ((high - value) * (mod / high))
    if mod < 0: 
        value = value + (value * mod)

    # the round is not very precise (bc of floats) but that's okay
    # ints: 0, floats: 3
    return round(value, round_dec)

def get_modified_chance(base_chance, positive_mods=[], negative_mods=[], values=[], mode='bayes'):
    """
    Bayesian updating model, based on an idea by my good friend Phil. Takes a 
    base chance of an event happening and applies the positive and negative 
    likelihoods to influence base chance given the event. 
    NOTE: all parameters are assumed to be positive floats between 0 and 1.
    """
    if mode == 'bayes':
        posterior = base_chance

        for (pos_lh, neg_lh, value) in zip(positive_mods, negative_mods, values):
            # Calculate likelihoods based on traits
            likelihood = pos_lh * value
            neg_likelihood = neg_lh * (1 - value)

            # Calculate marginal likelihood of the trait
            marginal = likelihood * posterior + neg_likelihood * (1 - posterior)
            
            # Update posterior probability using Bayes' Theorem
            posterior = (likelihood * posterior) / marginal
    
        return posterior
    
    else:
        # simple chance modifications with just the modifiers (no values)
        for positive_mod in positive_mod:
            base_chance = fair_mod(base_chance, positive_mod)
        for negative_mod in negative_mods:
            base_chance = fair_mod(base_chance, -1 * negative_mod)
        return base_chance

def get_vector_distance(element1, element2):
    """
    Returns vector distance between two sets of vector attributes. 
    """
    # convert input to vectors
    if isinstance(element1, dict):
        e1 = np.vector(element1.values())
    else:
        e1 = np.vector(element1)
    if isinstance(element2, dict):
        e2 = np.vector(element2.values())
    else:
        e2 = np.vector(element2)

    distance = np.linalg.norm(e2 - e1)
    return distance

"""
RANDOM NUMBERS & CHOICES
"""
def normal_in_range(loc, scale, upper=1, lower=0, round_dec=3):
    """
    Return random float from a normal distribution, within the specified range.
    """
    n = random.normal(loc, scale)
    # round happens now to avoid failed checks later
    n = round(n, round_dec)
    if n < lower:
        n = 0.
    elif n >= upper:
        under_bound = 0.1**round_dec
        n = round(upper - under_bound, round_dec)

    if round_dec == 0:
        return int(n)
    return n

def rand():
    """
    Return random float.
    """
    return random.random()

def rand_int(high, low=0):
    """
    Return random integer.
    """
    return random.randint(low, high)

def rand_choice(l, p=[], weights=[]):
    """
    Return random element from list weighted either by weights or a distribution.
    """
    if p != []:
        return random.choice(l, p=p)
    elif weights != []:
        w = weighted_choice(l, weights=weights)
        return w[0]
    return random.choice(l)

"""
PRINT HELP
"""
def beautify_print(d):
    """
    Properly print out a dict object with up to 2 nested dicts.
    """
    # could be implemented recursively?
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, dict):
                print(f"{k}:")
                for k2, v2 in v.items():
                    if isinstance(v2, dict): 
                        print(f"- {k2}:")
                        for k3, v3 in v2.items():
                            print(f"--- {k3} : {v3}")
                    else:
                        print(f"- {k2} : {v2}")
            else:
                print(f"{k} : {v}")
    elif isinstance(d, list):
        for i in d:
            print(i)
    else:
        print(d)

def print_dict_types(d : dict):
    """
    For debugging purposes (useful when json dumping)
    """
    for k, v in d.items():
        print(k)
        if isinstance(v, dict):
            for k2, v2 in v.items():
                print(k2)
                if isinstance(k2, dict):
                    for k3, v3 in v2:
                        print(type(k3), type(v3))
                else:
                    print(type(k2), type(v2))
        else:
            print(type(k), type(v))

"""
OTHER UTILS
"""
def fatal_error(msg): 
    print(msg)
    sys.exit()

def sexuality_match(sexA, sexB, sexualityA, sexualityB, mode='bool'):
    """
    TODO : score mode does not work well yet
    mode : ['bool', 'score']
    """
    if mode == 'bool': 
        if sexA != sexB:
            if sexualityA not in ['straight', 'bi']:
                return False
            if sexualityB not in ['straight', 'bi']:
                return False
            return True
        else:
            if sexualityA not in ['gay', 'bi']:
                return False
            if sexualityB not in ['gay', 'bi']:
                return False
            return True
    else:
        if sexA != sexB:
            if sexualityA < 0.75:
                a = 1 - sexualityA
            else:
                a = sexualityA
            if sexualityB < 0.75:
                b = 1 - sexualityB
            else:
                b = sexualityB
        else:
            if sexualityA < 0.75:
                a = sexualityA
            else:
                a = 1 - sexualityA
            if sexualityB < 0.75:
                b = sexualityB
            else:
                b = 1 - sexualityB
        return a * b

def age_match(ageA, ageB):
    """
    
    """
    elder = max(ageA, ageB)
    younger = min(ageA, ageB)
    match = 1
    
    if younger < 14:        
        difference = elder - younger
        for _ in range(difference):
            match *= 0.5
    else:
        rule_of_thumb = int((elder / 2) + 7)
        if younger < rule_of_thumb:
            adjusted_difference = rule_of_thumb - younger
            for _ in range(adjusted_difference):
                match *= 0.8
    return match
    

class MessageInbox():
    def __init__(self, owner) -> None:
        self.owner = owner
        self.inbox = []

    def add(self, msg: dict):
        self.inbox.append(msg)

    def get(self) -> dict:
        if not self.empty():
            msg = self.inbox.pop(0)
            return msg
        return None

    def empty(self) -> bool:
        if self.inbox == []:
            return True
        return False
