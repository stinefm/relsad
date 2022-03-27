import os
from relsad.network.systems import (
    PowerSystem,
)
from relsad.results.storage import (
    save_history,
)
from relsad.visualization.plotting import (
    plot_history,
    plot_history_last_state,
)
from relsad.Time import (
    Time,
    TimeUnit,
)


def update_history(
    power_system: PowerSystem,
    prev_time: Time,
    curr_time: Time,
    save_flag: bool,
):
    """
    Updates the history variables in the power system

    Parameters
    ----------
    power_system : PowerSystem
        A power system element
    prev_time : Time 
        The previous time
    curr_time : Time
        The current time
    save_flag : bool
        Indicates if saving is on of

    Returns
    ----------
    None

    """
    for network in power_system.child_network_list:
        for bus in network.buses:
            network.p_load_shed += bus.p_load_shed_stack
            network.q_load_shed += bus.q_load_shed_stack
        power_system.p_load_shed += network.p_load_shed
        power_system.q_load_shed += network.q_load_shed
        network.acc_p_load_shed += network.p_load_shed
        network.acc_q_load_shed += network.q_load_shed
    power_system.acc_p_load_shed += power_system.p_load_shed
    power_system.acc_q_load_shed += power_system.q_load_shed
    if save_flag:
        power_system_state_dict = {
            "p_load_shed": power_system.p_load_shed,
            "q_load_shed": power_system.p_load_shed,
            "acc_p_load_shed": power_system.acc_p_load_shed,
            "acc_q_load_shed": power_system.acc_q_load_shed,
            "p_load": power_system.get_system_load()[0],
            "q_load": power_system.get_system_load()[1],
        }
        for state_var, value in power_system_state_dict.items():
            power_system.history[state_var][curr_time] = value
        for network in power_system.child_network_list:
            network_state_dict = {
                "p_load_shed": network.p_load_shed,
                "q_load_shed": network.q_load_shed,
                "acc_p_load_shed": network.acc_p_load_shed,
                "acc_q_load_shed": network.acc_q_load_shed,
                "p_load": network.get_system_load()[0],
                "q_load": network.get_system_load()[1],
            }
            for state_var, value in network_state_dict.items():
                network.history[state_var][curr_time] = value
    power_system.p_load_shed = 0
    power_system.q_load_shed = 0
    for network in power_system.child_network_list:
        network.p_load_shed = 0
        network.q_load_shed = 0
    for comp in power_system.comp_list:
        comp.update_history(prev_time, curr_time, save_flag)
    power_system.controller.update_history(prev_time, curr_time, save_flag)


def plot_line_history(lines, save_dir: str):
    """
    Plots the history of the line in the power system

    Parameters
    ----------
    lines : list
        List of Line elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "p_from",
        "q_from",
        "p_to",
        "q_to",
        "remaining_outage_time",
        "failed",
        "line_loading",
    ]
    for state_var in whole_state_list:
        plot_history(lines, state_var, save_dir)


def save_line_history(lines, save_dir: str):
    """
    Saves the history of the line in the power system

    Parameters
    ----------
    lines : list
        List of Line elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "p_from",
        "q_from",
        "p_to",
        "q_to",
        "remaining_outage_time",
        "failed",
        "line_loading",
    ]
    for state_var in whole_state_list:
        save_history(lines, state_var, save_dir)


def plot_circuitbreaker_history(circuitbreakers, save_dir: str):
    """
    Plots the history of the circuitbreakers in the power system

    Parameters
    ----------
    circuitbreakers : list
        List of CircuitBreaker elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "is_open",
    ]
    for state_var in whole_state_list:
        plot_history(circuitbreakers, state_var, save_dir)


def save_circuitbreaker_history(circuitbreakers, save_dir: str):
    """
    Saves the history of the circuitbreakers in the power system

    Parameters
    ----------
    circuitbreakers : list
        List of CircuitBreaker elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "is_open",
    ]
    for state_var in whole_state_list:
        save_history(circuitbreakers, state_var, save_dir)


def plot_disconnector_history(disconnectors, save_dir: str):
    """
    Plots the history of the disconnectors in the power system

    Parameters
    ----------
    disconnectors: list
        List of Disconnector elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "is_open",
    ]
    for state_var in whole_state_list:
        plot_history(disconnectors, state_var, save_dir)


def save_disconnector_history(disconnectors, save_dir: str):
    """
    Saves the history of the disconnectors in the power system
    
    Parameters
    ----------
    disconnectors : list
        List of Disconnector elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "is_open",
    ]
    for state_var in whole_state_list:
        save_history(disconnectors, state_var, save_dir)


def plot_intelligent_switch_history(intelligent_switches, save_dir: str):
    """
    Plots the history of the intelligent switches in the power system
    
    Parameters
    ----------
    intelligent_switches : list
        List of IntelligentSwitch elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "remaining_repair_time",
        "state",
    ]
    for state_var in whole_state_list:
        plot_history(intelligent_switches, state_var, save_dir)


def save_intelligent_switch_history(intelligent_switches, save_dir: str):
    """
    Saves the history of the intelligent switches in the power system
    
    Parameters
    ----------
    intelligent_switches : list
        List of IntelligentSwitch elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "remaining_repair_time",
        "state",
    ]
    for state_var in whole_state_list:
        save_history(intelligent_switches, state_var, save_dir)


def plot_sensor_history(sensors, save_dir: str):
    """
    Plots the history of the sensors in the power system
    
    Parameters
    ----------
    sensors : list
        List of Sensor elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "remaining_repair_time",
        "state",
    ]
    for state_var in whole_state_list:
        plot_history(sensors, state_var, save_dir)


def save_sensor_history(sensors, save_dir: str):
    """
    Saves the history of the sensors in the power system
    
    Parameters
    ----------
    sensors : list
        List of Sensor elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "remaining_repair_time",
        "state",
    ]
    for state_var in whole_state_list:
        save_history(sensors, state_var, save_dir)


def plot_bus_history(buses, save_dir: str):
    """
    Plots the history of the buses in the power system
    
    Parameters
    ----------
    buses : list
        List of Bus elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "pload",
        "qload",
        "pprod",
        "qprod",
        "remaining_outage_time",
        "trafo_failed",
        "p_load_shed_stack",
        "q_load_shed_stack",
        "voang",
        "vomag",
    ]
    for state_var in whole_state_list:
        plot_history(buses, state_var, save_dir)
    last_state_list = [
        "acc_p_load_shed",
        "acc_q_load_shed",
        "avg_fail_rate",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
    ]
    for state_var in last_state_list:
        plot_history_last_state(buses, state_var, save_dir)


def save_bus_history(buses, save_dir: str):
    """
    Saves the history of the buses in the power system
    
    Parameters
    ----------
    buses : list
        List of Bus elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "pload",
        "qload",
        "pprod",
        "qprod",
        "remaining_outage_time",
        "trafo_failed",
        "p_load_shed_stack",
        "q_load_shed_stack",
        "voang",
        "vomag",
        "acc_p_load_shed",
        "acc_q_load_shed",
        "avg_fail_rate",
        "avg_outage_time",
        "acc_outage_time",
        "interruption_fraction",
    ]
    for state_var in whole_state_list:
        save_history(buses, state_var, save_dir)

def plot_ev_park_history(ev_parks, save_dir: str):
    """
    Plots the history of the ev_park in the power system
    
    Parameters
    ----------
    ev_parks : list
        List of EVPark elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "SOC",
        "ev_index",
        "demand",
        "charge",
        "num_cars",
        "interruption_fraction",
        "acc_interruptions",
        "acc_interruption_duration",
    ]
    for state_var in whole_state_list:
        plot_history(ev_parks, state_var, save_dir)


def save_ev_park_history(ev_parks, save_dir: str):
    """
    Saves the history of the ev_park in the power system
    
    Parameters
    ----------
    ev_parks : list
        List of EVPark elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "SOC",
        "ev_index",
        "demand",
        "charge",
        "num_cars",
        "interruption_fraction",
        "acc_interruptions",
        "acc_interruption_duration",
    ]
    for state_var in whole_state_list:
        save_history(ev_parks, state_var, save_dir)

def plot_battery_history(batteries, save_dir: str):
    """
    Plots the history of the battery in the power system
    
    Parameters
    ----------
    batteries : list
        List of Battery elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "SOC",
        "SOC_min",
        "remaining_survival_time",
    ]
    for state_var in whole_state_list:
        plot_history(batteries, state_var, save_dir)


def save_battery_history(batteries, save_dir: str):
    """
    Saves the history of the battery in the power system
    
    Parameters
    ----------
    batteries : list
        List of Battery elements
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "SOC",
        "SOC_min",
        "remaining_survival_time",
    ]
    for state_var in whole_state_list:
        save_history(batteries, state_var, save_dir)


def plot_power_system_history(power_system: PowerSystem, save_dir: str):
    """
    Plots the history of the power system
    
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
    whole_state_list = [
        "p_load_shed",
        "q_load_shed",
        "p_load",
        "q_load",
    ]
    power_system_save_dir = os.path.join(save_dir, power_system.name)
    for state_var in whole_state_list:
        plot_history([power_system], state_var, power_system_save_dir)
    for network in power_system.child_network_list:
        network_save_dir = os.path.join(save_dir, network.name)
        for state_var in whole_state_list:
            plot_history([network], state_var, network_save_dir)
    last_state_list = [
        "acc_p_load_shed",
        "acc_q_load_shed",
    ]
    power_system_save_dir = os.path.join(save_dir, power_system.name)
    for state_var in last_state_list:
        plot_history_last_state(
            [power_system], state_var, power_system_save_dir
        )
    for network in power_system.child_network_list:
        network_save_dir = os.path.join(save_dir, network.name)
        for state_var in last_state_list:
            plot_history_last_state([network], state_var, network_save_dir)


def save_power_system_history(power_system: PowerSystem, save_dir: str):
    """
    Saves the history of the power system
    
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
    whole_state_list = [
        "p_load_shed",
        "q_load_shed",
        "acc_p_load_shed",
        "acc_q_load_shed",
        "p_load",
        "q_load",
    ]
    power_system_save_dir = os.path.join(save_dir, power_system.name)
    for state_var in whole_state_list:
        save_history([power_system], state_var, power_system_save_dir)
    for network in power_system.child_network_list:
        network_save_dir = os.path.join(save_dir, network.name)
        for state_var in whole_state_list:
            save_history([network], state_var, network_save_dir)


def plot_network_controller_history(controllers, save_dir: str):
    """
    Plots the history of the controllers in the power system

    Parameters
    ----------
    controllers : list
        List of 
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "sectioning_time",
    ]
    for state_var in whole_state_list:
        plot_history(controllers, state_var, save_dir)


def save_network_controller_history(controllers, save_dir: str):
    """
    Saves the history of the controllers in the power system
    
    Parameters
    ----------
    controllers : list
        A power system element
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "sectioning_time",
    ]
    for state_var in whole_state_list:
        save_history(controllers, state_var, save_dir)


def plot_system_controller_history(controllers, save_dir: str):
    """
    Plots the history of the controllers in the power system
    
    Parameters
    ----------
    controllers : list
        A power system element
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "sectioning_time",
        "remaining_repair_time",
        "state",
    ]
    for state_var in whole_state_list:
        plot_history(controllers, state_var, save_dir)


def save_system_controller_history(controllers, save_dir: str):
    """
    Saves the history of the controllers in the power system
    
    Parameters
    ----------
    controllers : list
        A power system element
    save_dir : str
        The saving path

    Returns
    ----------
    None

    """
    whole_state_list = [
        "sectioning_time",
        "remaining_repair_time",
        "state",
    ]
    for state_var in whole_state_list:
        save_history(controllers, state_var, save_dir)
