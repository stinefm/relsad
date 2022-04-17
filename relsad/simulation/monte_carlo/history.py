import os
import copy
from relsad.Time import TimeUnit
from relsad.network.systems import (
    PowerSystem,
)
from relsad.network.components import (
    MainController,
)
from relsad.visualization.plotting import (
    plot_monte_carlo_history,
)
from relsad.results.storage import (
    save_monte_carlo_history,
    save_monte_carlo_history_from_dict,
)
from relsad.simulation.sequence.history import (
    save_power_system_history,
    save_bus_history,
    save_ev_park_history,
    save_battery_history,
    save_line_history,
    save_circuitbreaker_history,
    save_disconnector_history,
    save_intelligent_switch_history,
    save_sensor_history,
    save_network_controller_history,
    save_system_controller_history,
)
from relsad.reliability.indices import (
    SAIFI,
    SAIDI,
    CAIDI,
    EENS,
    EV_Index,
    EV_Interruption,
    EV_Duration,
)


def plot_network_monte_carlo_history(power_system: PowerSystem, save_dir: str):
    """
    Plots the history of the load shedding in the power system

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
        "acc_p_load_shed",
        "acc_q_load_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "EENS",
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
        "acc_p_load_shed",
        "acc_q_load_shed",
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
    power_system: PowerSystem, save_dir: str, save_dict: dict
):
    """
    Saves the history of the load shedding in the power system

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
        "acc_p_load_shed",
        "acc_q_load_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "EENS",
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
        "acc_p_load_shed",
        "acc_q_load_shed",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
        "acc_interruptions",
    ]
    for bus in power_system.buses:
        bus_save_dir = os.path.join(save_dir, bus.name)
        for state_var in bus_state_list:
            save_monte_carlo_history_from_dict(
                save_dict, [bus], state_var, bus_save_dir
            )


def initialize_history(power_system: PowerSystem):
    """
    Initializes the lists used for history variables

    Parameters
    ----------
    power_system : PowerSystem
        A power system element

    Returns
    ----------
    None

    """
    network_state_list = [
        "p_load_shed",
        "q_load_shed",
        "acc_p_load_shed",
        "acc_q_load_shed",
        "p_load",
        "q_load",
    ]
    for state_var in network_state_list:
        power_system.history[state_var] = {}
    for network in power_system.child_network_list:
        for state_var in network_state_list:
            network.history[state_var] = {}
    power_system.controller.initialize_history()


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
        "acc_p_load_shed",
        "acc_q_load_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "EENS",
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
        "acc_p_load_shed",
        "acc_q_load_shed",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
        "acc_interruptions",
    ]
    for bus in power_system.buses:
        save_dict[bus.name] = {}
        for state_var in bus_state_list:
            save_dict[bus.name][state_var] = {}
    return save_dict


def save_iteration_history(power_system: PowerSystem, it: int, save_dir: str):
    """
    Saves the history from an interation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it : int
        The iteration number
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    if not os.path.isdir(save_dir):
        os.makedirs(save_dir)
    if not os.path.isdir(os.path.join(save_dir, str(it))):
        os.mkdir(os.path.join(save_dir, str(it)))
    save_power_system_history(
        power_system,
        os.path.join(save_dir, str(it)),
    )
    save_bus_history(
        power_system.buses, os.path.join(save_dir, str(it), "bus")
    )
    if len(power_system.ev_parks) > 0:
        save_ev_park_history(
            power_system.ev_parks, os.path.join(save_dir, str(it), "ev_parks")
        )
    if len(power_system.batteries) > 0:
        save_battery_history(
            power_system.batteries, os.path.join(save_dir, str(it), "battery")
        )
    save_line_history(
        power_system.lines,
        os.path.join(save_dir, str(it), "line"),
    )
    if len(power_system.circuitbreakers) > 0:
        save_circuitbreaker_history(
            power_system.circuitbreakers,
            os.path.join(save_dir, str(it), "circuitbreaker"),
        )
    if len(power_system.disconnectors) > 0:
        save_disconnector_history(
            power_system.disconnectors,
            os.path.join(save_dir, str(it), "disconnector"),
        )

    if len(power_system.intelligent_switches) > 0:
        save_intelligent_switch_history(
            power_system.intelligent_switches,
            os.path.join(save_dir, str(it), "intelligent_switch"),
        )

    if len(power_system.sensors) > 0:
        save_sensor_history(
            power_system.sensors,
            os.path.join(save_dir, str(it), "sensor"),
        )

    if len(power_system.controller.distribution_controllers) > 0:
        save_network_controller_history(
            power_system.controller.distribution_controllers,
            os.path.join(save_dir, str(it), "distribution_controllers"),
        )

    if len(power_system.controller.microgrid_controllers) > 0:
        save_network_controller_history(
            power_system.controller.microgrid_controllers,
            os.path.join(save_dir, str(it), "microgrid_controllers"),
        )

    if isinstance(power_system.controller, MainController):
        save_system_controller_history(
            [power_system.controller],
            os.path.join(save_dir, str(it), "main_controller"),
        )


def update_monte_carlo_power_system_history(
    power_system: PowerSystem, it: int, time_unit: TimeUnit, save_dict: dict
):
    """
    Updates the history dictionary from the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it : int
        The iteration number
    time_unit : TimeUnit
        A time unit (hour, seconds, ect.)
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    network_state_dict = {
        "acc_p_load_shed": power_system.acc_p_load_shed,
        "acc_q_load_shed": power_system.acc_q_load_shed,
        "SAIFI": SAIFI(power_system),
        "SAIDI": SAIDI(power_system, time_unit),
        "CAIDI": CAIDI(power_system, time_unit),
        "EENS": EENS(power_system),
        "EV_Index": EV_Index(power_system),
        "EV_Interruption": EV_Interruption(power_system),
        "EV_Duration": EV_Duration(power_system, time_unit),
    }
    for state_var, value in network_state_dict.items():
        save_dict[power_system.name][state_var][it] = value
    save_dict = update_monte_carlo_child_network_history(
        power_system, it, time_unit, save_dict
    )
    save_dict = update_monte_carlo_comp_history(power_system, it, save_dict)
    return save_dict


def update_monte_carlo_child_network_history(
    power_system: PowerSystem, it: int, time_unit: TimeUnit, save_dict: dict
):
    """
    Updates the history dictionary for the child networks in the Monte Carlo simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    it : int
        The iteration number
    time_unit : TimeUnit
        A time unit (hour, seconds, ect.)
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    for network in power_system.child_network_list:
        network_state_dict = {
            "acc_p_load_shed": network.acc_p_load_shed,
            "acc_q_load_shed": network.acc_q_load_shed,
            "SAIFI": SAIFI(network),
            "SAIDI": SAIDI(network, time_unit),
            "CAIDI": CAIDI(network, time_unit),
            "EENS": EENS(network),
            "EV_Index": EV_Index(network),
            "EV_Interruption": EV_Interruption(network),
            "EV_Duration": EV_Duration(network, time_unit),
        }
        for state_var, value in network_state_dict.items():
            save_dict[network.name][state_var][it] = value
    return save_dict


def update_monte_carlo_comp_history(
    power_system: PowerSystem, it: int, save_dict: dict
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
            "acc_p_load_shed": bus.acc_p_load_shed,
            "acc_q_load_shed": bus.acc_q_load_shed,
            "avg_outage_time": bus.avg_outage_time,
            "acc_outage_time": bus.acc_outage_time,
            "interruption_fraction": bus.interruption_fraction,
            "acc_interruptions": bus.acc_interruptions,
        }
        for state_var, value in bus_state_dict.items():
            save_dict[bus.name][state_var][it] = value
    return save_dict


def merge_monte_carlo_history(
    power_system: PowerSystem, time_unit: TimeUnit, iteration_dicts: list
):
    """
    Merges the Monte Carlo history from all the iterations in the simulation

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    time_unit : TimeUnit
        A time unit (hour, seconds, ect.)
    iteration_dicts : list
        List containing information about all the iterations

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    save_dict = copy.deepcopy(iteration_dicts[0])
    network_state_dict = {
        "acc_p_load_shed": power_system.acc_p_load_shed,
        "acc_q_load_shed": power_system.acc_q_load_shed,
        "SAIFI": SAIFI(power_system),
        "SAIDI": SAIDI(power_system, time_unit),
        "CAIDI": CAIDI(power_system, time_unit),
        "EENS": EENS(power_system),
        "EV_Index": EV_Index(power_system),
        "EV_Interruption": EV_Interruption(power_system),
        "EV_Duration": EV_Duration(power_system, time_unit),
    }
    for it_dict in iteration_dicts:
        it = list(
            it_dict[power_system.name][
                list(network_state_dict.keys())[0]
            ].keys()
        )[0]
        for state_var in network_state_dict.keys():
            save_dict[power_system.name][state_var][it] = it_dict[
                power_system.name
            ][state_var][it]
        save_dict = merge_monte_carlo_child_network_history(
            power_system, it_dict, it, time_unit, save_dict
        )
        save_dict = merge_monte_carlo_comp_history(
            power_system, it_dict, it, save_dict
        )
    return save_dict


def merge_monte_carlo_child_network_history(
    power_system: PowerSystem,
    it_dict: dict,
    it: int,
    time_unit: TimeUnit,
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
    time_unit : TimeUnit
        Time unit
    save_dict : dict
        Dictionary with simulation results

    Returns
    ----------
    save_dict : dict
        Dictionary with simulation results

    """
    for network in power_system.child_network_list:
        network_state_dict = {
            "acc_p_load_shed": network.acc_p_load_shed,
            "acc_q_load_shed": network.acc_q_load_shed,
            "SAIFI": SAIFI(network),
            "SAIDI": SAIDI(network, time_unit),
            "CAIDI": CAIDI(network, time_unit),
            "EENS": EENS(network),
            "EV_Index": EV_Index(network),
            "EV_Interruption": EV_Interruption(network),
            "EV_Duration": EV_Duration(network, time_unit),
        }
        for state_var in network_state_dict.keys():
            save_dict[network.name][state_var][it] = it_dict[network.name][
                state_var
            ][it]
    return save_dict


def merge_monte_carlo_comp_history(
    power_system: PowerSystem, it_dict: dict, it: int, save_dict: dict
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
        bus_state_dict = {
            "acc_p_load_shed": bus.acc_p_load_shed,
            "acc_q_load_shed": bus.acc_q_load_shed,
            "avg_outage_time": bus.avg_outage_time,
            "acc_outage_time": bus.acc_outage_time,
            "interruption_fraction": bus.interruption_fraction,
            "acc_interruptions": bus.acc_interruptions,
        }
        for state_var in bus_state_dict.keys():
            save_dict[bus.name][state_var][it] = it_dict[bus.name][state_var][
                it
            ]
    return save_dict
