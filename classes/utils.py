import numpy as np
from numpy import random

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