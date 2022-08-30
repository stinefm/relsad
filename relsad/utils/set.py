"""
This module contains set operation utilities
"""


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
