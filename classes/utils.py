import numpy as np
from numpy import random
from random import choices as weighted_choice

"""
MODIFIERS
"""
def fair_mod(value, mod, high, round_dec=0):
    """
    Using fair math: 
    https://choicescriptdev.fandom.com/wiki/Arithmetic_operators#Fairmath
    """
    if mod > 0:
        value = value + ((high - value) * (mod / high))
    if mod < 0: 
        value = value + (value * mod)

    # the round is not very precise (bc of floats) but that's okay
    # ints: 0, floats: 3
    return round(value, round_dec)

def get_modified_chance(base_chance, positive_mods=[], negative_mods=[], mode='%'):
    return 

"""
RANDOM NUMBERS & CHOICES
"""
def normal_in_range(loc, scale, upper=1, lower=0, round_dec=3):
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
    return random.random()

def rand_int(high, low=0):
    return random.randint(low, high)

def rand_choice(l, p=[], weights=[]):
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


class MessageInbox():
    def __init__(self, owner) -> None:
        self.owner = owner
        self.inbox = []

    def add(self, msg: dict):
        self.inbox.append(msg)

    def get(self) -> dict:
        if not self.empty():
            return self.inbox[0]

    def empty(self) -> bool:
        if self.inbox == []:
            return True
        return False
