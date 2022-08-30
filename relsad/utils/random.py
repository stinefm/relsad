"""
This module contains random utilities
"""

import numpy as np

from relsad.Time import Time


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


def convert_yearly_fail_rate(fail_rate_per_year: float, dt: Time):
    """
    Returns the failure rate of the time increment, dt, based on
    the given yearly failure rate

    Parameters
    ----------
    fail_rate_per_year : float
        The failure rate
    dt : Time
        The current time step

    Returns
    -------
    fail_rate : float
        The converted failure rate for time increment, dt
    """
    fail_rate = min(fail_rate_per_year * dt.get_years(), 1)
    return fail_rate
