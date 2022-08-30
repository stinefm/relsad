import os

import pandas as pd


def save_monte_carlo_history_from_dict(
    save_dict: dict,
    comp_list: list,
    attribute: str,
    save_dir: str,
):
    """
    Saves history from dictionary to files

    Parameters
    ----------
    save_dict : dict
        Dictionary with simulation results
    comp_list : list
        A list of system componets
    attribute : str
        A system attribute
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """

    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    df = pd.DataFrame()
    for comp in comp_list:
        data = save_dict[comp.name][attribute]
        df[comp] = data.values()
    df.index = data.keys()
    df.index.name = "it"
    df.to_csv(os.path.join(save_dir, attribute + ".csv"))
