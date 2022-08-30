import os

import pandas as pd

from relsad.Time import TimeUnit


def save_history(
    obj_list: list,
    attribute: str,
    time_unit: TimeUnit,
    save_dir: str,
):
    """
    Saves history to files

    Parameters
    ----------
    obj_list : list
        A list of relsad objects
    attribute : str
        A system attribute
    time_unit : TimeUnit
        The time unit of the simulation
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    df = pd.DataFrame()
    for obj in obj_list:
        data = obj.get_history(attribute)
        df[obj] = data.values()
    df.index = data.keys()
    df.index.name = time_unit.name
    df.to_csv(os.path.join(save_dir, attribute + ".csv"))
