def flatten(toflatten: list):
    """
    Function that flattens nested list, handy for printing

    Parameters
    ----------
    toflatten : list
        Nested list

    Returns
    -------
    None

    """
    for element in toflatten:
        try:
            yield from flatten(element)
        except TypeError:
            yield element
