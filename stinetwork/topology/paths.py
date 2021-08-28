import itertools
from stinetwork.network.components import Line
from stinetwork.network.systems import Section
from stinetwork.utils import unique, intersection


def get_paths(parent_bus):
    """Function that finds all downstream paths in a radial tree

    Input:
    parent_bus(Bus): Parent bus of radial tree

    Output:
    paths(list): List of all downstream paths from parent_bus

    """
    if len(parent_bus.nextbus) == 0:
        return [[[parent_bus]]]
    paths = []
    for nbus in parent_bus.nextbus:
        for path in get_paths(nbus):
            paths.append([[parent_bus]] + path)
    return paths


def get_line_paths(parent_line):
    """Function that finds all downstream paths in a radial tree

    Input:
    parent_line(Line): Parent line of radial tree

    Output:
    paths(list): List of all downstream paths from parent_bus

    """
    if len(parent_line.tbus.fromline_list) == 0:
        return [[parent_line]]
    paths = []
    for nbus in parent_line.tbus.fromline_list:
        for path in get_line_paths(nbus):
            paths.append([parent_line] + path)
    return paths


def create_sections(
    connected_line: Line, lines: list, sections: list, rank: int = 0
):
    if sections == []:
        lines = unique(
            itertools.chain.from_iterable(get_line_paths(connected_line))
        )
        section = Section(rank, lines)
        sections.append(section)
        sections = create_sections(
            connected_line, [connected_line], sections, rank + 1
        )
    else:
        curr_lines = connected_line.tbus.fromline_list
        for curr_line in curr_lines:
            next_lines = curr_line.tbus.fromline_list
            if next_lines != []:
                if curr_line.disconnectors == []:
                    sections = create_sections(
                        curr_line, lines, sections, rank
                    )
                else:
                    if len(curr_line.disconnectors) == 2:
                        section = Section(rank + 1, [curr_line])
                        sections.append(section)
                        sections = unique(sections)
                    for discon in curr_line.disconnectors:
                        if discon.base_bus == curr_line.fbus:
                            lines = unique(
                                itertools.chain.from_iterable(
                                    get_line_paths(curr_line)
                                )
                            )
                            section = Section(rank, lines)
                            sections.append(section)
                            sections = unique(sections)
                            sections = create_sections(
                                curr_line, [curr_line], sections, rank + 1
                            )
                        elif discon.base_bus == curr_line.tbus:
                            for next_line in next_lines:
                                lines = unique(
                                    itertools.chain.from_iterable(
                                        get_line_paths(next_line)
                                    )
                                )
                                section = Section(rank, lines)
                                sections.append(section)
                                sections = unique(sections)
                                sections = create_sections(
                                    next_line, [next_line], sections, rank + 1
                                )
    return sections


# flake8: noqa: C901
def configure(bus_list, line_list):
    """Function that sets up the nested topology array and configures the radial tree according to the slack bus"""

    def line_between_buses(bus1, bus2, line_list):
        for line in line_list:
            if (line.tbus == bus1 and line.fbus == bus2) or (
                line.tbus == bus2 and line.fbus == bus1
            ):
                return line

    def change_dir(target_buses, bus_list, checked_buses, line_list):
        new_target_buses = list()
        for target_bus in target_buses:
            if target_bus not in checked_buses:
                for bus in bus_list:
                    if bus not in checked_buses and bus != target_bus:
                        line = line_between_buses(target_bus, bus, line_list)
                        if line is not None:
                            if target_bus in bus.nextbus:
                                line.change_direction()
                            new_target_buses.append(bus)
                            new_target_buses = unique(new_target_buses)
                checked_buses.append(target_bus)
                checked_buses = unique(checked_buses)
        return new_target_buses, checked_buses

    def get_topology(paths):
        """Function that constructs a nested topology array

        Input:
        paths(list): List of all downstream paths from parent_bus in radial tree

        Output:
        topology(list): Nested topology list
        """
        used_buses = list()
        main_path = paths[0]
        used_buses += main_path
        topology = [main_path]
        for path in paths[1:]:
            sub_path = list()
            for bus in path:
                if bus not in used_buses:
                    sub_path.append(bus)
            used_buses += sub_path
            if sub_path != list():
                topology.append(sub_path)

        while len(topology) > 1:
            last_path = topology[-1]
            top_bus = last_path[0][0]
            for n, path in enumerate(topology[:-1]):
                for k, bus in enumerate(path):
                    if top_bus in bus[0].nextbus:
                        topology[n][k].append(last_path)
                        topology.remove(last_path)
                        break

        topology = topology[0]

        return topology

    ## Find slack bus
    for i, bus in enumerate(bus_list):
        if bus.is_slack:
            slack_bus = bus
            old = bus_list[0]
            bus_list[0] = slack_bus
            bus_list[i] = old
            break

    ## Update directions based on slack bus (making slack bus parent of the radial tree)
    checked_buses = list()
    target_buses, checked_buses = change_dir(
        [slack_bus], bus_list, checked_buses, line_list
    )
    while target_buses != list():
        target_buses, checked_buses = change_dir(
            target_buses, bus_list, checked_buses, line_list
        )

    paths = get_paths(slack_bus)

    topology = get_topology(paths)

    return topology, bus_list, line_list


def flatten(toflatten):
    """
    Function that flattens nested list, handy for printing
    """
    for element in toflatten:
        try:
            yield from flatten(element)
        except TypeError:
            yield element


def find_backup_lines_between_sub_systems(sub_system1, sub_system2):
    """
    Finds connections between sub systems
    """

    def find_external_backup_lines(sub_system):
        """
        Finds lines connected to sub system buses that are connecte to external sub systems
        """
        external_backup_lines = list()
        for bus in sub_system.buses:
            for line in bus.connected_lines:
                if line not in sub_system.lines and line.is_backup:
                    external_backup_lines.append(line)
                    external_backup_lines = unique(external_backup_lines)
        return external_backup_lines

    external_backup_lines1 = find_external_backup_lines(sub_system1)
    external_backup_lines2 = find_external_backup_lines(sub_system2)
    # Returns
    return intersection(external_backup_lines1, external_backup_lines2)
