from relsad.network.components import Bus, Line
from relsad.utils import unique


def get_downstream_buses(parent_bus: Bus):
    """
    Function that finds and returns all downstream buses in a radial tree

    Parameters
    ----------
    parent_bus : Bus
        Parent bus of radial tree

    Returns
    -------
    downstream_buses : list
        List of all downstream buses from parent_bus

    """
    if len(parent_bus.nextbus) == 0:
        return [[[parent_bus]]]
    downstream_buses = []
    for nbus in parent_bus.nextbus:
        for downstream_bus in get_downstream_buses(nbus):
            downstream_buses.append([[parent_bus]] + downstream_bus)
    return downstream_buses


def configure_bfs_load_flow_setup(
    bus_list: list,
    line_list: list,
):
    """
    Function that sets up the nested topology array and configures the radial tree according to the slack bus

    Parameters
    ----------
    bus_list : list
        List containing the bus elements
    line_list : list
        List containing the line elements

    Returns
    -------
    topology : list
        Nested topology list
    bus_list : list
        Updated bus list

    """

    ## Find slack bus
    for i, bus in enumerate(bus_list):
        if bus.is_slack:
            slack_bus = bus
            old = bus_list[0]
            bus_list[0] = slack_bus
            bus_list[i] = old
            break

    # Update directions based on slack bus
    # (making slack bus parent of the radial tree)
    update_line_direction_based_on_slack_bus(slack_bus, bus_list, line_list)

    downstream_bus_list = get_downstream_buses(slack_bus)

    topology_bus_list = get_topology_bus_list(downstream_bus_list)

    return topology_bus_list, bus_list


def line_between_buses(
    bus1: Bus,
    bus2: Bus,
    line_list: list,
):
    """
    Returns the line between two buses (bus1 and bus2)
    if it exists, else None

    Parameters
    ----------
    bus1 : Bus
        A Bus element
    bus2 : Bus
        A Bus elememt
    line_list : list
        List containing all the lines

    Returns
    -------
    line : Line
        The line between bus1 and bus2

    """
    for line in line_list:
        if (line.tbus == bus1 and line.fbus == bus2) or (
            line.tbus == bus2 and line.fbus == bus1
        ):
            return line
    return None


def update_line_direction_based_on_slack_bus(
    slack_bus: Bus,
    bus_list: list,
    line_list: list,
):
    """
    Update line directions based on slack bus
    (making slack bus parent of the radial tree)

    Parameters
    ----------
    slack_bus : Bus
        Slack bus
    bus_list : list
        List containing buses
    line_list : list
        List containing lines

    Returns
    -------
    None

    """
    target_buses = [slack_bus]
    used_target_buses = list()
    while target_buses != list():
        new_target_buses = list()
        for target_bus in target_buses:
            if target_bus not in used_target_buses:
                for bus in bus_list:
                    if bus not in used_target_buses and bus != target_bus:
                        line = line_between_buses(target_bus, bus, line_list)
                        if line is not None:
                            if target_bus in bus.nextbus:
                                line.change_direction()
                            new_target_buses.append(bus)
                            new_target_buses = unique(new_target_buses)
                used_target_buses.append(target_bus)
                used_target_buses = unique(used_target_buses)
        target_buses = new_target_buses


def get_topology_bus_list(downstream_bus_list: list):
    """
    Function that constructs a nested topology bus list

    Parameters
    ----------
    downstream_bus_list : list
        Nested list of all downstream buses from parent_bus
        in radial tree

    Returns
    ----------
    topology_bus_list : list
        Nested topology list

    """
    used_buses = list()
    main_downstream_bus_list = downstream_bus_list[0]
    used_buses += main_downstream_bus_list
    topology_bus_list = [main_downstream_bus_list]
    for downstream_child_bus_list in downstream_bus_list[1:]:
        sub_downstream_bus_list = list()
        for bus in downstream_child_bus_list:
            if bus not in used_buses:
                sub_downstream_bus_list.append(bus)
        used_buses += sub_downstream_bus_list
        if sub_downstream_bus_list != list():
            topology_bus_list.append(sub_downstream_bus_list)

    while len(topology_bus_list) > 1:
        last_downstream_bus_list = topology_bus_list[-1]
        top_bus = last_downstream_bus_list[0][0]
        for n, downstream_child_bus_list in enumerate(topology_bus_list[:-1]):
            for k, bus in enumerate(downstream_child_bus_list):
                if top_bus in bus[0].nextbus:
                    topology_bus_list[n][k].append(last_downstream_bus_list)
                    topology_bus_list.remove(last_downstream_bus_list)
                    break

    topology_bus_list = topology_bus_list[0]

    return topology_bus_list
