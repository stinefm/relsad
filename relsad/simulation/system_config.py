import numpy as np

from relsad.network.components import Bus, MicrogridMode
from relsad.network.systems import PowerSystem, SubSystem, Transmission
from relsad.Time import Time, TimeStamp, TimeUnit
from relsad.topology.sub_systems import find_backup_lines_between_sub_systems
from relsad.utils import subtract, unique


def find_sub_systems(p_s: PowerSystem, curr_time: Time):
    """
    Function that finds the independent sub systems of the given power system
    and adds them to the sub_systems list of the power system

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem object
    curr_time : Time
        Current time

    Returns
    ----------
    None

    """

    p_s.sub_systems = []
    # Will only include connected lines
    active_lines = [line for line in p_s.lines if line.connected]
    used_buses = []
    used_lines = []
    sub_system = SubSystem()

    while not (len(used_buses) + len(used_lines)) == (
        len(p_s.buses) + len(active_lines)
    ):
        for bus in p_s.buses:
            if bus not in unique(used_buses + sub_system.buses):
                if (len(sub_system.buses) + len(sub_system.lines)) == 0:
                    sub_system, used_buses = add_bus(
                        p_s,
                        bus,
                        sub_system,
                        used_buses,
                    )
                    (
                        sub_system,
                        used_buses,
                        used_lines,
                    ) = try_to_add_connected_lines(
                        p_s,
                        bus,
                        sub_system,
                        used_buses,
                        used_lines,
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


def try_to_add_connected_lines(
    p_s: PowerSystem,
    bus: Bus,
    sub_system: SubSystem,
    used_buses: list,
    used_lines: list,
):
    """
    Add lines to the sub system

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem object
    bus : Bus
        A Bus object
    sub_system : SubSystem
        A SubSystem object
    used_buses : list
        List of used Bus elements
    used_lines : list
        List of used Line elements

    Returns
    ----------
    sub_system : SubSystem
        A SubSystem object
    used_buses : list
        List of used Bus elements
    used_lines : list
        List of used Line elements

    """
    for line in subtract(bus.connected_lines, used_lines):
        if line.connected:
            sub_system.add_line(line)
            used_lines.append(line)
            used_lines = unique(used_lines)
            if line.tbus == bus:
                sub_system, used_buses = add_bus(
                    p_s,
                    line.fbus,
                    sub_system,
                    used_buses,
                )
                (
                    sub_system,
                    used_buses,
                    used_lines,
                ) = try_to_add_connected_lines(
                    p_s,
                    line.fbus,
                    sub_system,
                    used_buses,
                    used_lines,
                )
            else:
                sub_system, used_buses = add_bus(
                    p_s,
                    line.tbus,
                    sub_system,
                    used_buses,
                )
                (
                    sub_system,
                    used_buses,
                    used_lines,
                ) = try_to_add_connected_lines(
                    p_s,
                    line.tbus,
                    sub_system,
                    used_buses,
                    used_lines,
                )
    return sub_system, used_buses, used_lines


def add_bus(
    p_s: PowerSystem,
    bus: Bus,
    sub_system: SubSystem,
    used_buses: list,
):
    """
    Add buses to the sub system

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem object
    bus : Bus
        A Bus object
    sub_system : SubSystem
        A SubSystem object
    used_buses : list
        List of used Bus elements

    Returns
    ----------
    sub_system : SubSystem
        A SubSystem object
    used_buses : list
        List of used Bus elements

    """
    if bus not in unique(used_buses + sub_system.buses):
        sub_system.add_bus(bus)
        used_buses.append(bus)
        used_buses = unique(used_buses)
        for child_network in p_s.child_network_list:
            if bus in child_network.buses:
                sub_system.add_child_network(child_network)
    return sub_system, used_buses


def update_backup_lines_between_sub_systems(p_s: PowerSystem, curr_time: Time):
    """
    Function that updates the backup lines between the sub systems
    of the power system if they exist and are not failed

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem element
    curr_time : Time
        Current time

    Returns
    ----------
    None

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
                        and all(
                            [
                                x.parent_network.controller.sectioning_time
                                <= Time(0)
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
    Function that updates the current slack bus of the sub systems of the power system

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem element

    Returns
    ----------
    None

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

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem element
    sub_system : SubSystem
        A SubSystem element

    Returns
    ----------
    bool
        Success/Failure of operation

    """
    ## Transmission network slack buses in sub_system
    for bus in sub_system.buses:
        for child_network in p_s.child_network_list:
            if isinstance(child_network, Transmission):
                if bus == child_network.get_trafo_bus():
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
                    bus.battery.mode == MicrogridMode.LIMITED_SUPPORT
                    and bus.battery.remaining_survival_time == Time(0)
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
    ## Buses with EV_park
    if sub_system.slack is None:
        for bus in sub_system.buses:
            if bus.ev_park is not None and bus.ev_park.v2g_flag is True:
                bus.set_slack()
                sub_system.slack = bus
                return True
    ## Not slack material
    return False


def prepare_system(
    power_system: PowerSystem,
    start_time: TimeStamp,
    stop_time: TimeStamp,
    time_step: Time,
    time_unit: TimeUnit,
):
    """
    Prepares the power system for a simulation by:
     - Creating system sections based on switches
     - Defining the simulation time increments
     - Interpolating load and production data based on
       the time increments

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem element
    start_time : TimeStamp
        The start time of the simulation/iteration
    stop_time : TimeStamp
        The stop time of the simulation/iteration
    time_step : Time
        A time step (1 hour, 2 hours, ect.)
    time_unit : TimeUnit
        A time unit (hour, seconds, ect.)

    Returns
    ----------
    time_array:
        Array containing the time increments of the simulation

    """
    # Create power system sections
    power_system.create_sections()

    # Set up time increments based on defined period
    increments = int((stop_time - start_time) / time_step)
    sim_duration = increments * time_step.get_unit_quantity(time_unit)
    time_array = np.arange(
        start=time_step.get_unit_quantity(time_unit),
        stop=sim_duration,
        step=time_step.get_unit_quantity(time_unit),
    )
    time_array_indices = np.arange(increments)

    # Prepare load and production data
    power_system.prepare_load_data(time_array_indices)
    power_system.prepare_prod_data(time_array_indices)

    return time_array


def reset_system(power_system: PowerSystem, save_flag: bool):
    """
    Resets the power system

    Parameters
    ----------
    p_s : PowerSystem
        A PowerSystem element
    save_flag : bool
        Indicates if saving is on or off

    Returns
    ----------
    None

    """
    power_system.reset_energy_shed_variables()
    for network in power_system.child_network_list:
        network.reset_energy_shed_variables()

    for comp in power_system.comp_list:
        comp.reset_status(save_flag)
    power_system.controller.reset_status(save_flag)

    ## Find sub systems
    find_sub_systems(power_system, 0)
    update_sub_system_slack(power_system)
