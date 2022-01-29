"""
This module contains package utils
"""

import numpy as np
from .Time import Time

# Numerical value used as "infinite", choose it based on system values
INF = 1e8

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


def eq(x: float, y: float, tol: float = 1e-6):
    """
    Checks for equality within a tolerance
    """
    return abs(x - y) < tol


def random_choice(random_instance: np.random.Generator, p_true: float):
    """
    Returns random choice based on uniform probability distribution
    """
    return random_instance.random() < p_true


def interpolate(array: np.ndarray, time_indices: np.ndarray):
    return np.interp(time_indices, np.arange(array.size), array)


def convert_yearly_fail_rate(fail_rate_per_year: float, dt: Time):
    return fail_rate_per_year * dt.get_hours() / (365 * 24)


if __name__ == "__main__":
    pass
