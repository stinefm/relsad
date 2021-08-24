import os
import copy
from stinetwork.network.systems import (
    PowerSystem,
)
from stinetwork.visualization.plotting import (
    plot_monte_carlo_history,
)
from stinetwork.results.storage import (
    save_monte_carlo_history,
    save_monte_carlo_history_from_dict,
)
from stinetwork.simulation.sequence.history import (
    save_power_system_history,
    save_bus_history,
    save_battery_history,
    save_line_history,
    save_circuitbreaker_history,
    save_disconnector_history,
)
from stinetwork.reliability.indices import (
    SAIFI,
    SAIDI,
    CAIDI,
    EENS,
)


def plot_network_monte_carlo_history(power_system: PowerSystem, save_dir: str):
    """
    Plots the history of the load shedding in the power system
    """
    network_state_list = [
        "acc_p_load_shed",
        "acc_q_load_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "EENS",
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
    ]
    for bus in power_system.buses:
        bus_save_dir = os.path.join(save_dir, bus.name)
        for state_var in bus_state_list:
            save_monte_carlo_history_from_dict(
                save_dict, [bus], state_var, bus_save_dir
            )


def initialize_history(power_system: PowerSystem):
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


def initialize_monte_carlo_history(power_system: PowerSystem):
    network_state_list = [
        "acc_p_load_shed",
        "acc_q_load_shed",
        "SAIFI",
        "SAIDI",
        "CAIDI",
        "EENS",
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
    ]
    for bus in power_system.buses:
        save_dict[bus.name] = {}
        for state_var in bus_state_list:
            save_dict[bus.name][state_var] = {}
    return save_dict


def save_iteration_history(power_system: PowerSystem, it: int, save_dir: str):
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


def update_monte_carlo_history(
    power_system: PowerSystem, it: int, save_dict: dict
):
    network_state_dict = {
        "acc_p_load_shed": power_system.acc_p_load_shed,
        "acc_q_load_shed": power_system.acc_q_load_shed,
        "SAIFI": SAIFI(power_system),
        "SAIDI": SAIDI(power_system),
        "CAIDI": CAIDI(power_system),
        "EENS": EENS(power_system),
    }
    for state_var, value in network_state_dict.items():
        save_dict[power_system.name][state_var][it] = value
    save_dict = update_monte_carlo_child_network_history(
        power_system, it, save_dict
    )
    save_dict = update_monte_carlo_comp_history(power_system, it, save_dict)
    return save_dict


def update_monte_carlo_child_network_history(
    power_system: PowerSystem, it: int, save_dict: dict
):
    for network in power_system.child_network_list:
        network_state_dict = {
            "acc_p_load_shed": network.acc_p_load_shed,
            "acc_q_load_shed": network.acc_q_load_shed,
            "SAIFI": SAIFI(network),
            "SAIDI": SAIDI(network),
            "CAIDI": CAIDI(network),
            "EENS": EENS(network),
        }
        for state_var, value in network_state_dict.items():
            save_dict[network.name][state_var][it] = value
    return save_dict


def update_monte_carlo_comp_history(
    power_system: PowerSystem, it: int, save_dict: dict
):
    for bus in power_system.buses:
        bus_state_dict = {
            "acc_p_load_shed": bus.acc_p_load_shed,
            "acc_q_load_shed": bus.acc_q_load_shed,
            "avg_outage_time": bus.avg_outage_time,
        }
        for state_var, value in bus_state_dict.items():
            save_dict[bus.name][state_var][it] = value
    return save_dict


def merge_monte_carlo_history(
    power_system: PowerSystem, iteration_dicts: list
):
    save_dict = copy.deepcopy(iteration_dicts[0])
    network_state_dict = {
        "acc_p_load_shed": power_system.acc_p_load_shed,
        "acc_q_load_shed": power_system.acc_q_load_shed,
        "SAIFI": SAIFI(power_system),
        "SAIDI": SAIDI(power_system),
        "CAIDI": CAIDI(power_system),
        "EENS": EENS(power_system),
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
            power_system, it_dict, it, save_dict
        )
        save_dict = merge_monte_carlo_comp_history(
            power_system, it_dict, it, save_dict
        )
    return save_dict


def merge_monte_carlo_child_network_history(
    power_system: PowerSystem, it_dict: dict, it: int, save_dict: dict
):
    for network in power_system.child_network_list:
        network_state_dict = {
            "acc_p_load_shed": network.acc_p_load_shed,
            "acc_q_load_shed": network.acc_q_load_shed,
            "SAIFI": SAIFI(network),
            "SAIDI": SAIDI(network),
            "CAIDI": CAIDI(network),
            "EENS": EENS(network),
        }
        for state_var in network_state_dict.keys():
            save_dict[network.name][state_var][it] = it_dict[network.name][
                state_var
            ][it]
    return save_dict


def merge_monte_carlo_comp_history(
    power_system: PowerSystem, it_dict: dict, it: int, save_dict: dict
):
    for bus in power_system.buses:
        bus_state_dict = {
            "acc_p_load_shed": bus.acc_p_load_shed,
            "acc_q_load_shed": bus.acc_q_load_shed,
            "avg_outage_time": bus.avg_outage_time,
        }
        for state_var in bus_state_dict.keys():
            save_dict[bus.name][state_var][it] = it_dict[bus.name][state_var][
                it
            ]
    return save_dict
