import pandas as pd
import os


def save_history(comp_list: list, attribute: str, save_dir: str):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    df = pd.DataFrame()
    for comp in comp_list:
        data = comp.get_history(attribute)
        df[comp] = data.values()
    df.index = data.keys()
    df.to_csv(os.path.join(save_dir, attribute + ".csv"))


def save_monte_carlo_history(comp_list: list, attribute: str, save_dir: str):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    df = pd.DataFrame()
    for comp in comp_list:
        data = comp.get_monte_carlo_history(attribute)
        df[comp] = data.values()
    df.index = data.keys()
    df.to_csv(os.path.join(save_dir, attribute + ".csv"))


def save_monte_carlo_history_from_dict(
    save_dict: dict, comp_list: list, attribute: str, save_dir: str
):
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    df = pd.DataFrame()
    for comp in comp_list:
        data = save_dict[comp.name][attribute]
        df[comp] = data.values()
    df.index = data.keys()
    df.to_csv(os.path.join(save_dir, attribute + ".csv"))


if __name__ == "__main__":
    pass
