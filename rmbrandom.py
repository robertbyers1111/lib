#!/bin/env python3

from random import randint, random, seed
from datetime import datetime
from rmblogging import Rmblogging, LogLevels, debug, info, notice, warning, error


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def randval_0_to_1():
    """
    Generate a random float value x, such that 0.0 <= x < 1.0
    """
    seed(datetime.now().strftime('%f%S%M%H'))
    randomvalue = random()
    debug(f"returning random float: {randomvalue}")
    return randomvalue


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
def randval_int(bounds):
    """
    Generate a random integer i, such that A <= i < B, where A is the first element of bounds, B is the second
    """
    A = bounds[0]
    B = bounds[1]
    debug(f"Generating a random integer in the range {A}-{B}")
    debug(f"Seeding random number generator..")
    seed(datetime.now().strftime('%f%S%M%H'))
    debug(f"Generating the random integer..")
    randomvalue = randint(A, B-1)
    debug(f"Random integer is {randomvalue}")
    debug(f"Returning {randomvalue}")
    return randomvalue

