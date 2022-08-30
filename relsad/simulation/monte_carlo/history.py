import copy
import os

from relsad.network.systems import PowerSystem
from relsad.reliability.indices import (
    ASAI,
    ASUI,
    CAIDI,
    ENS,
    SAIDI,
    SAIFI,
    EV_Duration,
    EV_Index,
    EV_Interruption,
)
from relsad.results.storage import save_monte_carlo_history_from_dict
from relsad.Time import Time
from relsad.visualization.plotting import plot_monte_carlo_history


def plot_network_monte_carlo_history(power_system: PowerSystem, save_dir: str):
    """
    Plots the history of the energy.shedding in the power system

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    network_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "ASAI",
        "ASUI",
        "ENS",
        "EV_Index",
        "EV_Interruption",
        "EV_Duration",
    ]
    power_system_save_dir = os.path.join(save_dir, power_system.name)
    for state_var in network_state_list:
        plot_monte_carlo_history(
            [power_system], state_var, power_system_save_dir
        )
    for network in power_system.child_network_list:
        network_save_dir = os.path.join(save_dir, network.name)
        for state_var in network_state_list:
            plot_monte_carlo_history([network], state_var, network_save_dir)
    bus_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
        "acc_interruptions",
    ]
    for bus in power_system.buses:
        bus_save_dir = os.path.join(save_dir, bus.name)
        for state_var in bus_state_list:
            plot_monte_carlo_history([bus], state_var, bus_save_dir)


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
    network_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "ASAI",
        "ASUI",
        "ENS",
        "EV_Index",
        "EV_Interruption",
        "EV_Duration",
    ]
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
    bus_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
        "acc_interruptions",
    ]
    ev_park_state_list = [
        "acc_num_interruptions",
        "acc_exp_interruptions",
        "acc_exp_car_interruptions",
        "acc_interruption_duration",
        "acc_available_num_cars",
        "num_cars",
    ]
    for bus in power_system.buses:
        bus_save_dir = os.path.join(save_dir, bus.name)
        for state_var in bus_state_list:
            save_monte_carlo_history_from_dict(
                save_dict, [bus], state_var, bus_save_dir
            )
        if bus.ev_park is not None:
            ev_park_save_dir = os.path.join(bus_save_dir, bus.ev_park.name)
            for state_var in ev_park_state_list:
                save_monte_carlo_history_from_dict(
                    save_dict, [bus.ev_park], state_var, ev_park_save_dir
                )


def initialize_monte_carlo_history(power_system: PowerSystem):
    """
    Initializes the lists used for history variables from the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    network_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "ASAI",
        "ASUI",
        "ENS",
        "EV_Index",
        "EV_Interruption",
        "EV_Duration",
    ]
    save_dict = {}
    save_dict[power_system.name] = {}
    for state_var in network_state_list:
        save_dict[power_system.name][state_var] = {}
    for network in power_system.child_network_list:
        save_dict[network.name] = {}
        for state_var in network_state_list:
            save_dict[network.name][state_var] = {}
    bus_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
        "acc_interruptions",
    ]
    ev_park_state_list = [
        "acc_num_interruptions",
        "acc_exp_interruptions",
        "acc_exp_car_interruptions",
        "acc_interruption_duration",
        "acc_available_num_cars",
        "num_cars",
    ]
    for bus in power_system.buses:
        save_dict[bus.name] = {}
        for state_var in bus_state_list:
            save_dict[bus.name][state_var] = {}
        if bus.ev_park is not None:
            save_dict[bus.ev_park.name] = {}
            for state_var in ev_park_state_list:
                save_dict[bus.ev_park.name][state_var] = {}
    return save_dict


def update_monte_carlo_power_system_history(
    power_system: PowerSystem,
    it: int,
    current_time: Time,
    save_dict: dict,
):
    """
    Updates the history dictionary from the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it : int
        The iteration number
    current_time : Time
        Current time
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    network_state_dict = {
        "acc_p_energy_shed": power_system.acc_p_energy_shed,
        "acc_q_energy_shed": power_system.acc_q_energy_shed,
        "SAIFI": SAIFI(power_system),
        "SAIDI": SAIDI(power_system),
        "CAIDI": CAIDI(power_system),
        "ASAI": ASAI(power_system, current_time),
        "ASUI": ASUI(power_system, current_time),
        "ENS": ENS(power_system),
        "EV_Index": EV_Index(power_system),
        "EV_Interruption": EV_Interruption(power_system),
        "EV_Duration": EV_Duration(power_system),
    }
    for state_var, value in network_state_dict.items():
        save_dict[power_system.name][state_var][it] = value
    save_dict = update_monte_carlo_child_network_history(
        power_system, it, current_time, save_dict
    )
    save_dict = update_monte_carlo_comp_history(power_system, it, save_dict)
    return save_dict


def update_monte_carlo_child_network_history(
    power_system: PowerSystem,
    it: int,
    current_time: Time,
    save_dict: dict,
):
    """
    Updates the history dictionary for the child networks in the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it : int
        The iteration number
    current_time : Time
        Current time
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    for network in power_system.child_network_list:
        network_state_dict = {
            "acc_p_energy_shed": network.acc_p_energy_shed,
            "acc_q_energy_shed": network.acc_q_energy_shed,
            "SAIFI": SAIFI(network),
            "SAIDI": SAIDI(network),
            "CAIDI": CAIDI(network),
            "ASAI": ASAI(network, current_time),
            "ASUI": ASUI(network, current_time),
            "ENS": ENS(network),
            "EV_Index": EV_Index(network),
            "EV_Interruption": EV_Interruption(network),
            "EV_Duration": EV_Duration(network),
        }
        for state_var, value in network_state_dict.items():
            save_dict[network.name][state_var][it] = value
    return save_dict


def update_monte_carlo_comp_history(
    power_system: PowerSystem,
    it: int,
    save_dict: dict,
):
    """
    Updates the component values for the system from the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
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
        bus_state_dict = {
            "acc_p_energy_shed": bus.acc_p_energy_shed,
            "acc_q_energy_shed": bus.acc_q_energy_shed,
            "avg_outage_time": bus.avg_outage_time.get_hours(),
            "acc_outage_time": bus.acc_outage_time.get_hours(),
            "interruption_fraction": bus.interruption_fraction,
            "acc_interruptions": bus.acc_interruptions,
        }
        for state_var, value in bus_state_dict.items():
            save_dict[bus.name][state_var][it] = value
        if bus.ev_park is not None:
            ev_park_state_dict = {
                "acc_num_interruptions": bus.ev_park.acc_num_interruptions,
                "acc_exp_interruptions": bus.ev_park.acc_exp_interruptions,
                "acc_exp_car_interruptions": bus.ev_park.acc_exp_car_interruptions,
                "acc_interruption_duration": bus.ev_park.acc_interruption_duration.get_hours(),
                "acc_available_num_cars": bus.ev_park.acc_available_num_cars,
                "num_cars": bus.ev_park.num_cars,
            }
            for state_var, value in ev_park_state_dict.items():
                save_dict[bus.ev_park.name][state_var][it] = value
    return save_dict


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
    network_state_list = [
        "acc_p_energy_shed",
        "acc_q_energy_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "ASAI",
        "ASUI",
        "ENS",
        "EV_Index",
        "EV_Interruption",
        "EV_Duration",
    ]
    for it_dict in iteration_dicts:
        it = list(it_dict[power_system.name][network_state_list[0]].keys())[0]
        for state_var in network_state_list:
            save_dict[power_system.name][state_var][it] = it_dict[
                power_system.name
            ][state_var][it]
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
    Initializes the lists used for history variables from the Monte Carlo simulation

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
        network_state_list = [
            "acc_p_energy_shed",
            "acc_q_energy_shed",
            "SAIFI",
            "SAIDI",
            "CAIDI",
            "ASAI",
            "ASUI",
            "ENS",
            "EV_Index",
            "EV_Interruption",
            "EV_Duration",
        ]
        for state_var in network_state_list:
            save_dict[network.name][state_var][it] = it_dict[network.name][
                state_var
            ][it]
    return save_dict


def merge_monte_carlo_comp_history(
    power_system: PowerSystem,
    it_dict: dict,
    it: int,
    save_dict: dict,
):
    """
    Initializes the lists used for history variables from the Monte Carlo simulation

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
        bus_state_list = [
            "acc_p_energy_shed",
            "acc_q_energy_shed",
            "avg_outage_time",
            "acc_outage_time",
            "interruption_fraction",
            "acc_interruptions",
        ]
        for state_var in bus_state_list:
            save_dict[bus.name][state_var][it] = it_dict[bus.name][state_var][
                it
            ]
        if bus.ev_park is not None:
            ev_park_state_list = [
                "acc_num_interruptions",
                "acc_exp_interruptions",
                "acc_exp_car_interruptions",
                "acc_interruption_duration",
                "acc_available_num_cars",
                "num_cars",
            ]
            for state_var in ev_park_state_list:
                save_dict[bus.ev_park.name][state_var][it] = it_dict[
                    bus.ev_park.name
                ][state_var][it]
    return save_dict
