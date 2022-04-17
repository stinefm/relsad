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

    Parameters
    ----------
    sequence :

    Returns
    ----------
    None

    """
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def subtract(list1, list2):
    """
    Return difference between lists while preserving the order

    Parameters
    ----------
    list1 : list
    list2 : list

    Returns
    ----------
    difference :

    """

    difference = [x for x in list1 if x not in list2]
    return difference


def intersection(list1, list2):
    """
    Returns the intersection between two list while preserving the order

    Parameters
    ----------
    list1 : list
    list2 : list

    Returns
    ----------
    None
    """

    return [x for x in list1 if x in list2]


def random_instance(seed=None):
    """
    Return a numpy random instance with optional seed

    Parameters
    ----------
    seed : int

    Returns
    ----------
    None
    """
    return np.random.default_rng(seed)


def eq(x: float, y: float, tol: float = 1e-6):
    """
    Checks for equality within a tolerance

    Parameters
    ----------
    x : float
    y : float
    tol : float

    Returns
    ----------
    None
    """
    return abs(x - y) < tol


def random_choice(random_instance: np.random.Generator, p_true: float):
    """
    Returns random choice based on uniform probability distribution

    Parameters
    ----------
    random_instance : np.random.Generator
    p_true : float

    Returns
    ----------
    None
    """
    return random_instance.random() < p_true


def interpolate(array: np.ndarray, time_indices: np.ndarray):
    """
    Returns random choice based on uniform probability distribution

    arameters
    ----------
    array : np.ndarray
    time_indices : np.ndarray

    Returns
    ----------
    None
    """
    return np.interp(time_indices, np.arange(array.size), array)


def convert_yearly_fail_rate(fail_rate_per_year: float, dt: Time):
    """
    Returns random choice based on uniform probability distribution

    Parameters
    ----------
    fail_rate_per_year : float
        The failure rate
    dt : Time
        The current time step

    Returns
    ----------
    choice : float
        Random choice
    """
    choice = min(fail_rate_per_year * dt.get_years(), 1)
    return choice


if __name__ == "__main__":
    pass
