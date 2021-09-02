import itertools
from stinetwork.network.components import Line
from stinetwork.network.containers import Section
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
    lines = [
        x
        for x in parent_line.tbus.fromline_list
        if x in parent_line.parent_network.lines
    ]
    if len(lines) == 0:
        return [[parent_line]]
    paths = []
    for nline in lines:
        for path in get_line_paths(nline):
            paths.append([parent_line] + path)
    return paths


def create_downstream_sections(
    curr_line: Line, parent_section: Section = None
):
    if not parent_section:
        lines = unique(
            itertools.chain.from_iterable(get_line_paths(curr_line))
        )
        disconnectors = (
            curr_line.disconnectors + curr_line.circuitbreaker.disconnectors
            if curr_line.circuitbreaker != None
            else curr_line.disconnectors
        )
        parent_section = Section(None, lines, disconnectors)
        parent_section = create_downstream_sections(curr_line, parent_section)
    else:
        next_lines = [
            x
            for x in curr_line.tbus.fromline_list
            if x in curr_line.parent_network.lines
        ]
        if next_lines != []:
            for next_line in next_lines:
                if next_line.disconnectors == []:
                    parent_section = create_downstream_sections(
                        next_line, parent_section
                    )
                else:
                    lines = unique(
                        itertools.chain.from_iterable(
                            get_line_paths(next_line)
                        )
                    )
                    section = Section(
                        parent_section, lines, next_line.disconnectors
                    )
                    section = create_downstream_sections(next_line, section)
                    parent_section.add_child_section(section)
                    if len(next_line.disconnectors) > 1 and lines != [
                        next_line
                    ]:
                        child_section = Section(
                            section, [next_line], next_line.disconnectors
                        )
                        section.add_child_section(child_section)
    return parent_section


def create_internal_sections(parent_section):
    child_lines = set(
        itertools.chain.from_iterable(
            [x.lines for x in parent_section.child_sections]
        )
    )
    lines = list(set(parent_section.lines) - child_lines)
    child_sections = parent_section.child_sections
    for child_section in child_sections:
        child_section = create_internal_sections(child_section)
    if lines == [] and parent_section.parent != None:
        parent_section.parent.child_sections.remove(parent_section)
        parent_section = parent_section.parent
        for child_section in child_sections:
            if not child_section in parent_section.child_sections:
                parent_section.child_sections.append(child_section)
        parent_section = create_internal_sections(parent_section)
    else:
        parent_section.lines = lines
        parent_section.disconnectors = unique(
            parent_section.disconnectors
            + [
                x
                for child_section in parent_section.child_sections
                for x in child_section.disconnectors
                if x.line in parent_section.lines
                or sum(
                    [
                        l in parent_section.lines
                        for l in x.line.fbus.toline_list
                    ]
                )
                > 0
            ]
        )
    if len(parent_section.lines) == 1:
        if len(parent_section.lines[0].disconnectors) > 0:
            parent_section.disconnectors = (
                parent_section.lines[0].disconnectors
                + parent_section.lines[0].circuitbreaker.disconnectors
                if parent_section.lines[0].circuitbreaker != None
                else parent_section.lines[0].disconnectors
            )
    return parent_section


def get_section_list(parent_section, section_list=[]):
    if section_list == []:
        section_list.append(parent_section)
    section_list += parent_section.child_sections
    for child in parent_section.child_sections:
        section_list = get_section_list(child, section_list)
    return section_list


def create_sections(connected_line):
    parent_section = create_downstream_sections(connected_line, [])
    parent_section = create_internal_sections(parent_section)
    parent_section.attach_to_lines()
    return parent_section


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
