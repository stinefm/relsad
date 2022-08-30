"""
This module contains array utilities
"""

import numpy as np


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
