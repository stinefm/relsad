import os

from relsad.network.components import MainController
from relsad.network.systems import PowerSystem
from relsad.results.storage import save_history
from relsad.Time import TimeUnit
from relsad.visualization.plotting import plot_history


def plot_obj_history(
    obj_list: list,
    time_unit: TimeUnit,
    save_dir: str,
):
    """
    Plots the history of a list of objects in the power system

    Parameters
    ----------
    obj_list : list
        List of objects
    time_unit : TimeUnit
        The time unit of the simulation
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """
    for attribute in obj_list[0].history:
        plot_history(
            obj_list=obj_list,
            time_unit=time_unit,
            attribute=attribute,
            save_dir=save_dir)


def save_obj_history(
    obj_list: list,
    time_unit: TimeUnit,
    save_dir: str,
):
    """
    Saves the history of a list of objects in the power system

    Parameters
    ----------
    obj_list : list
        List of objects
    time_unit : TimeUnit
        The time unit of the simulation
    save_dir : str
        The saving directory

    Returns
    ----------
    None

    """
    for attribute in obj_list[0].history:
        save_history(
            obj_list=obj_list,
            attribute=attribute,
            time_unit=time_unit,
            save_dir=save_dir,
        )


def save_sequence_history(
    power_system: PowerSystem,
    time_unit: TimeUnit,
    save_dir: str,
):
    """
    Saves the history from an sequence

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    time_unit : TimeUnit
        The time unit of the simulation
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    # Power system
    save_obj_history(
        obj_list=[power_system],
        time_unit=time_unit,
        save_dir=os.path.join(save_dir, power_system.name),
    )
    # Child networks
    for network in power_system.child_network_list:
        save_obj_history(
            obj_list=[network],
            time_unit=time_unit,
            save_dir=os.path.join(save_dir, network.name),
        )
    # Buses
    comp_save_dict = {
        "bus": power_system.buses,
        "ev_parks": power_system.ev_parks,
        "battery": power_system.batteries,
        "line": power_system.lines,
        "circuitbreaker": power_system.circuitbreakers,
        "disconnector": power_system.disconnectors,
        "intelligent_switch": power_system.intelligent_switches,
        "sensor": power_system.sensors,
        "distribution_controllers": power_system.controller.distribution_controllers,
        "microgrid_controllers": power_system.controller.microgrid_controllers,
        "main_controller": (
            [power_system.controller]
            if isinstance(power_system.controller, MainController)
            else []
        ),
        "ict_line": power_system.ict_lines,
        "ict_node": power_system.ict_nodes,
    }

    for obj_name, obj_list in comp_save_dict.items():
        if len(obj_list) > 0:
            save_obj_history(
                obj_list=obj_list,
                time_unit=time_unit,
                save_dir=os.path.join(save_dir, obj_name),
            )
