"""
This module contains package utils
"""

import numpy as np


def unique(sequence):
    """
    Return list of unique elements while preserving the order
    """
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def subtract(list1, list2):
    """
    Return difference between lists while preserving the order
    """
    return [x for x in list1 if x not in list2]


def intersection(list1, list2):
    """
    Returns the intersection between two list while preserving the order
    """
    return [x for x in list1 if x in list2]


def random_instance(seed=None):
    """
    Return a numpy random instance with optional seed
    """
    return np.random.default_rng(seed)


def eq(x: float, y: float):
    """
    Checks for equality within a tolerance
    """
    return abs(x - y) < 1e-6

def random_choice(
    """
    Returns random choice based on uniform probability distribution
    """
    random_instance: np.random.Generator, 
    p_true: float):
    return random_instance.random() < p_true


if __name__ == "__main__":
    pass
