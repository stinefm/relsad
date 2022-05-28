"""
This module contains package utils
"""

import numpy as np
from .Time import Time

# Numerical value used as "infinite", choose it based on system values
INF = 1e8


def unique(sequence: list):
    """
    Return list of unique elements while preserving the order

    Parameters
    ----------
    sequence : list
        List of elements

    Returns
    -------
    unq : list
        List of unique elements with preserved order

    """
    seen = set()
    unq = [x for x in sequence if not (x in seen or seen.add(x))]
    return unq


def subtract(list1: list, list2: list):
    """
    Return difference between lists while preserving the order

    Parameters
    ----------
    list1 : list
    list2 : list

    Returns
    -------
    difference : list
        The difference between lists with preserved order

    """

    difference = [x for x in list1 if x not in list2]
    return difference


def intersection(list1: list, list2: list):
    """
    Returns the intersection between two list while preserving the order

    Parameters
    ----------
    list1 : list
        List 1
    list2 : list
        List 2

    Returns
    -------
    intersec : list
        The intersection between two list with preserved order

    """
    intersec = [x for x in list1 if x in list2]

    return intersec


def get_random_instance(seed: int = None):
    """
    Return a numpy random instance with optional seed

    Parameters
    ----------
    seed : int
        Random seed

    Returns
    -------
    random_instance : numpy.random.Generator
        Random instance generator

    """
    random_instance = np.random.default_rng(seed)
    return random_instance


def eq(x: float, y: float, tol: float = 1e-6):
    """
    Checks for equality within a tolerance

    Parameters
    ----------
    x : float
        Left hand side
    y : float
        Right hand side
    tol : float
        The equality tolerance

    Returns
    -------
    equal : bool
        Boolean variable stating whether the left and right hand side
        are equal within the given tolerance

    """
    equal = abs(x - y) < tol
    return equal


def random_choice(random_instance: np.random.Generator, p_true: float):
    """
    Returns random choice based on uniform probability distribution

    Parameters
    ----------
    random_instance : np.random.Generator
        Instance of a random generator
    p_true : float
        The probability of true

    Returns
    -------
    choice : bool
        Random choice based on uniform probability distribution

    """
    if random_instance is None:
        random_instance = get_random_instance()
    choice = random_instance.random() < p_true
    return choice


def interpolate(array: np.ndarray, time_indices: np.ndarray):
    """
    Returns the array interpolated to match the time indices

    arameters
    ----------
    array : np.ndarray
        Array to interpolate
    time_indices : np.ndarray
        Array of required time indices in need of array values

    Returns
    -------
    interpolated_array : np.ndarray
        The array interpolated to match the time indices

    """
    x = np.linspace(0, array.size - 1, time_indices.size)
    interpolated_array = np.interp(x, np.arange(array.size), array)
    return interpolated_array


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
    -------
    choice : float
        Random choice
    """
    choice = min(fail_rate_per_year * dt.get_years(), 1)
    return choice


if __name__ == "__main__":
    pass
