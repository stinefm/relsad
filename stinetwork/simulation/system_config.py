from stinetwork.network.systems import (
    PowerSystem,
    SubSystem,
    Transmission,
)
from stinetwork.utils import (
    unique,
    subtract,
)
from stinetwork.topology.paths import find_backup_lines_between_sub_systems
from stinetwork.simulation.monte_carlo.history import initialize_history


def find_sub_systems(p_s: PowerSystem, curr_time):
    """
    Function that find the independent sub systems of the given power system
    and adds them to the sub_systems list of the power system
    """

    p_s.sub_systems = list()
    # Will only include connected lines
    active_lines = [line for line in p_s.lines if line.connected]
    used_buses = list()
    used_lines = list()
    sub_system = SubSystem()

    def try_to_add_connected_lines(bus, sub_system, used_buses, used_lines):
        for line in subtract(bus.connected_lines, used_lines):
            if line.connected:
                sub_system.add_line(line)
                used_lines.append(line)
                used_lines = unique(used_lines)
                if line.tbus == bus:
                    sub_system, used_buses = add_bus(
                        line.fbus, sub_system, used_buses
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        line.fbus, sub_system, used_buses, used_lines
                    )
                else:
                    sub_system, used_buses = add_bus(
                        line.tbus, sub_system, used_buses
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        line.tbus, sub_system, used_buses, used_lines
                    )
        return sub_system, used_buses, used_lines

    def add_bus(bus, sub_system, used_buses):
        if bus not in unique(used_buses + sub_system.buses):
            sub_system.add_bus(bus)
            used_buses.append(bus)
            used_buses = unique(used_buses)
            for child_network in p_s.child_network_list:
                if bus in child_network.buses:
                    sub_system.add_child_network(child_network)
        return sub_system, used_buses

    while not (len(used_buses) + len(used_lines)) == (
        len(p_s.buses) + len(active_lines)
    ):
        for bus in p_s.buses:
            if bus not in unique(used_buses + sub_system.buses):
                if (len(sub_system.buses) + len(sub_system.lines)) == 0:
                    sub_system, used_buses = add_bus(
                        bus, sub_system, used_buses
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        bus, sub_system, used_buses, used_lines
                    )
                    p_s.sub_systems.append(sub_system)
                    p_s.sub_systems = unique(p_s.sub_systems)
                    if (len(used_buses) + len(used_lines)) == (
                        len(p_s.buses) + len(active_lines)
                    ):
                        break
                    sub_system = SubSystem()

    if len(p_s.sub_systems) > 1:
        update_backup_lines_between_sub_systems(p_s, curr_time)


def update_backup_lines_between_sub_systems(p_s: PowerSystem, curr_time):
    """
    Function that updates the backup lines between the sub systems of the
    power system if they exist and are not failed
    """
    update = False
    for s_1 in p_s.sub_systems:
        for s_2 in p_s.sub_systems:
            if s_1 != s_2:
                external_backup_lines = find_backup_lines_between_sub_systems(
                    s_1, s_2
                )
                for line in external_backup_lines:
                    if (
                        not line.connected
                        and not line.failed
                        and sum(
                            [
                                not x.section.connected if x.section else False
                                for x in line.tbus.connected_lines
                                + line.fbus.connected_lines
                            ]
                        )
                        == 0
                        and all(
                            [
                                x.parent_network.controller.remaining_section_time
                                == 0
                                for x in line.tbus.connected_lines
                                + line.fbus.connected_lines
                            ]
                        )
                    ):
                        for discon in line.get_disconnectors():
                            if discon.is_open:
                                discon.close()
                        update = True
                        break
            if update:
                break
        if update:
            break
    if update:
        find_sub_systems(p_s, curr_time)


def update_sub_system_slack(p_s: PowerSystem):
    """
    Function that updates the current slack bus of the sub systems of the
    power system
    """
    possible_sub_systems = list(p_s.sub_systems)
    for sub_system in possible_sub_systems:
        sub_system.slack = None
        for bus in sub_system.buses:
            bus.is_slack = False
            if set_slack(p_s, sub_system):
                break


def set_slack(p_s: PowerSystem, sub_system: SubSystem):
    """
    Function that sets the slack bus of the power system
    """
    ## Transmission network slack buses in sub_system
    for bus in sub_system.buses:
        for child_network in p_s.child_network_list:
            if type(child_network) == Transmission:
                if bus == child_network.get():
                    bus.set_slack()
                    sub_system.slack = bus
                    return True
    ## Buses with battery
    if sub_system.slack is None:
        for bus in sub_system.buses:
            if (
                bus.battery is not None and bus.battery.mode is None
            ):  # Battery in Distribution network
                bus.set_slack()
                sub_system.slack = bus
                return True
        for bus in sub_system.buses:
            if (
                bus.battery is not None and bus.battery.mode is not None
            ):  # Battery in Microgrid
                if (
                    bus.battery.mode == "limited support"
                    and bus.battery.remaining_survival_time == 0
                    and not bus.is_slack
                ):
                    bus.battery.start_survival_time()
                bus.set_slack()
                sub_system.slack = bus
                return True
    ## Buses with production
    if sub_system.slack is None:
        for bus in sub_system.buses:
            if bus.prod is not None:
                bus.set_slack()
                sub_system.slack = bus
                return True
    ## Not slack material
    return False


def reset_system(power_system: PowerSystem, save_flag: bool):
    power_system.reset_load_shed_variables()
    for network in power_system.child_network_list:
        network.reset_load_shed_variables()
    initialize_history(power_system)

    for comp in power_system.comp_list:
        comp.reset_status(save_flag)

    ## Find sub systems
    find_sub_systems(power_system, 0)
    update_sub_system_slack(power_system)
