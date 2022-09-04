import copy
import os

from relsad.network.systems import PowerSystem
from relsad.results.storage import save_monte_carlo_history_from_dict


def save_network_monte_carlo_history(
    power_system: PowerSystem,
    save_dir: str,
    save_dict: dict,
):
    """
    Saves the history of the energy.shedding in the power system

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    save_dir : str
        The saving path
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    network_state_list = list(save_dict[power_system.name].keys())
    power_system_save_dir = os.path.join(save_dir, power_system.name)
    for state_var in network_state_list:
        save_monte_carlo_history_from_dict(
            save_dict, [power_system], state_var, power_system_save_dir
        )
    for network in power_system.child_network_list:
        network_save_dir = os.path.join(save_dir, network.name)
        for state_var in network_state_list:
            save_monte_carlo_history_from_dict(
                save_dict, [network], state_var, network_save_dir
            )
    for bus in power_system.buses:
        bus_save_dir = os.path.join(save_dir, bus.name)
        bus_state_list = list(save_dict[bus.name].keys())
        for state_var in bus_state_list:
            save_monte_carlo_history_from_dict(
                save_dict, [bus], state_var, bus_save_dir
            )
        if bus.ev_park is not None:
            ev_park_save_dir = os.path.join(bus_save_dir, bus.ev_park.name)
            ev_park_state_list = list(save_dict[bus.ev_park.name].keys())
            for state_var in ev_park_state_list:
                save_monte_carlo_history_from_dict(
                    save_dict, [bus.ev_park], state_var, ev_park_save_dir
                )


def merge_monte_carlo_history(
    power_system: PowerSystem,
    iteration_dicts: list,
):
    """
    Merges the Monte Carlo history from all the iterations in the simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    iteration_dicts : list
        List containing information about all the iterations

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    save_dict = copy.deepcopy(iteration_dicts[0])
    for it_dict in iteration_dicts:
        curr_it_dict = it_dict[power_system.name]
        network_state_list = list(curr_it_dict.keys())
        it = list(curr_it_dict[network_state_list[0]].keys())[0]
        for state_var in network_state_list:
            save_dict[power_system.name][state_var][it] = (
                curr_it_dict[state_var][it]
            )
        save_dict = merge_monte_carlo_child_network_history(
            power_system, it_dict, it, save_dict
        )
        save_dict = merge_monte_carlo_comp_history(
            power_system, it_dict, it, save_dict
        )
    return save_dict


def merge_monte_carlo_child_network_history(
    power_system: PowerSystem,
    it_dict: dict,
    it: int,
    save_dict: dict,
):
    """
    Merges the lists used for history variables from the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it_dict : dict
        Dictionary with iteration results
    it : int
        Iteration number
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    for network in power_system.child_network_list:
        curr_it_dict = it_dict[network.name]
        network_state_list = list(curr_it_dict.keys())
        for state_var in network_state_list:
            save_dict[network.name][state_var][it] = (
                curr_it_dict[state_var][it]
            )
    return save_dict


def merge_monte_carlo_comp_history(
    power_system: PowerSystem,
    it_dict: dict,
    it: int,
    save_dict: dict,
):
    """
    Merges the lists used for component history variables
    from the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it_dict : dict
        Dictionary with iteration results
    it : int
        The iteration number
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    for bus in power_system.buses:
        curr_bus_it_dict = it_dict[bus.name]
        bus_state_list = list(curr_bus_it_dict.keys())
        for state_var in bus_state_list:
            save_dict[bus.name][state_var][it] = (
                curr_bus_it_dict[state_var][it]
            )
        if bus.ev_park is not None:
            curr_ev_park_it_dict = it_dict[bus.ev_park.name]
            ev_park_state_list = list(curr_ev_park_it_dict.keys())
            for state_var in ev_park_state_list:
                save_dict[bus.ev_park.name][state_var][it] = (
                    curr_ev_park_it_dict[state_var][it]
                )
    return save_dict
