"""
This module contains comparison utilities
"""


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
