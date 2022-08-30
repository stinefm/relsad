import os

import matplotlib.pyplot as plt
import pandas as pd

from relsad.Time import TimeUnit


def plot_history(
    obj_list: list,
    attribute: str,
    time_unit: TimeUnit,
    save_dir: str,
):
    """
    Plots the history

    Parameters
    ----------
    obj_list : list
        List of objects
    attribute : str
        An attribute
    time_unit : TimeUnit
        The time unit of the simulation
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    for obj in obj_list:
        data = obj.get_history(attribute)
        ax.plot(list(data.values()), label=obj.name)
    ax.set_title(attribute)
    ax.set_xlabel(time_unit.name)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


def plot_monte_carlo_history(
    obj_list: list,
    attribute: str,
    save_dir: str,
):
    """
    Plots the history from the Monte Carlo simulation

    Parameters
    ----------
    obj_list : list
        List of objects
    attribute : str
        An attribute
    save_dir : str
        The saving directory

    Returns
    ----------
    None


    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    for obj in obj_list:
        data = obj.get_monte_carlo_history(attribute)
        ax.plot(list(data.values()), label=obj.name)
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)


def plot_history_last_state(
    obj_list: list,
    attribute: str,
    save_dir: str,
):
    """
    Plots the last state from the history

    Parameters
    ----------
    obj_list : list
        List of objects
    attribute : str
        An attribute
    save_dir : str
        The saving directory

    Returns
    ----------
    None


    """
    if not os.path.isdir(save_dir):
        os.mkdir(save_dir)
    fig = plt.figure(dpi=150)
    ax = fig.add_subplot(1, 1, 1)
    df = pd.DataFrame()
    for obj in obj_list:
        data = obj.get_history(attribute)
        df[obj] = data.values()
    df.iloc[-1].plot.bar()
    ax.set_title(attribute)
    ax.legend()
    fig.savefig(os.path.join(save_dir, attribute + ".pdf"), format="pdf")
    plt.close(fig)
