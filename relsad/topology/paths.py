import itertools
from relsad.network.components import Bus, Line
from relsad.network.containers import Section
from relsad.network.systems import SubSystem
from relsad.utils import unique, intersection


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


def get_downstream_lines(parent_line: Line):
    """
    Function that finds and returns all downstream lines in a radial tree

    Parameters
    ----------
    parent_line : Line
        Parent line of radial tree

    Returns
    -------
    downstream_lines : list
        List of all downstream lines from parent_line

    """
    lines = [
        x
        for x in parent_line.tbus.fromline_list
        if x in parent_line.parent_network.lines
    ]
    if len(lines) == 0:
        return [[parent_line]]
    downstream_lines = []
    for nline in lines:
        for downstream_line in get_downstream_lines(nline):
            downstream_lines.append([parent_line] + downstream_line)
    return downstream_lines


def create_downstream_sections(
    curr_line: Line,
    parent_section: Section = None,
):
    """
    Creates sections downstream from the current line

    Parameters
    ----------
    curr_line : Line
        The current line
    parent_section : Section
        The parent section

    Returns
    -------
    parent_section : Section
        The updated parent section

    """
    if parent_section is None:
        # No parent section, gathers all downstream lines and
        # disconnectors to create a parent section
        lines = unique(
            itertools.chain.from_iterable(get_downstream_lines(curr_line))
        )
        disconnectors = (
            curr_line.disconnectors + curr_line.circuitbreaker.disconnectors
            if curr_line.circuitbreaker is not None
            else curr_line.disconnectors
        )
        parent_section = Section(None, lines, disconnectors)
        parent_section = create_downstream_sections(curr_line, parent_section)
    else:
        # A parent section exists, gathers all downstream lines and
        # disconnectors to create a downstream child section
        next_lines = [
            x
            for x in curr_line.tbus.fromline_list
            if x in curr_line.parent_network.lines
        ]
        if next_lines != []:
            # Not an end line, continues searching for
            # disconnectors in downstream lines
            for next_line in next_lines:
                if next_line.disconnectors == []:
                    # Line without a disconnector, continue
                    # searching downstream
                    parent_section = create_downstream_sections(
                        next_line, parent_section
                    )
                else:
                    # Line with a disconnector, gather downstream
                    # lines and disconnectors for a new child section
                    lines = unique(
                        itertools.chain.from_iterable(
                            get_downstream_lines(next_line)
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
                        # Multiple disconnectors on line (that is not an end line)
                        # Add a child section containing line and disconnectors
                        child_section = Section(
                            section, [next_line], next_line.disconnectors
                        )
                        section.add_child_section(child_section)
    return parent_section


def refine_sections(
    parent_section: Section,
):
    """
    Refines the sections within the parent section including the parent
    section itself. Removes unnecessary coarse sections. Returns the
    refined parent section.

    Parameters
    ----------
    parent_section : Section
        The parent section

    Returns
    -------
    parent_section : Section
        The refined parent section

    """
    # Finds the unique lines of the parent section
    # not shared by any of the child sections
    child_lines = set(
        itertools.chain.from_iterable(
            [x.lines for x in parent_section.child_sections]
        )
    )
    lines = list(set(parent_section.lines) - child_lines)

    # Creates internal sections recursively in
    # the child sections
    child_sections = parent_section.child_sections
    for child_section in child_sections:
        child_section = refine_sections(child_section)

    if lines == [] and parent_section.parent is not None:
        # No unique parent section lines, parent section
        # covered by its child sections and thus unnecessary
        # Removes parent section
        parent_section.parent.child_sections.remove(parent_section)
        # Adds current child sections to the parent of the removed
        # parent section
        parent_section = parent_section.parent
        for child_section in child_sections:
            if child_section not in parent_section.child_sections:
                parent_section.child_sections.append(child_section)
        parent_section = refine_sections(parent_section)
    else:
        # Parent section has unique lines
        # Remove non-unique lines and disconnectors from
        # parent section
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
                        toline in parent_section.lines
                        for toline in x.line.fbus.toline_list
                    ]
                )
                > 0
            ]
        )
    if len(parent_section.lines) == 1:
        if len(parent_section.lines[0].disconnectors) > 0:
            # Single line parent section with disconnector(s)
            # Adds circuitbreaker disconnectors if line
            # contains circuitbreaker
            parent_section.disconnectors = (
                parent_section.lines[0].disconnectors
                + parent_section.lines[0].circuitbreaker.disconnectors
                if parent_section.lines[0].circuitbreaker is not None
                else parent_section.lines[0].disconnectors
            )
    return parent_section


def get_section_list(
    parent_section: Section,
    section_list: list = [],
):
    """
    Appends and returns a list containing the sections in the path

    Parameters
    ----------
    parent_section : Section
        The parent section
    section_list : list
        List containing the sections

    Returns
    -------
    section_list : list
        List containing the sections

    """
    if section_list == []:
        section_list.append(parent_section)
    section_list += parent_section.child_sections
    for child in parent_section.child_sections:
        section_list = get_section_list(child, section_list)
    return section_list


def create_sections(connected_line: Line):
    """
    Create layered network sections starting downstream from the network connected line.
    The sections are separated by disconnectors.

    Parameters
    ----------
    connected_line : Line
        The line connecting the network to the parent network

    Returns
    -------
    parent_section : Section
        The parent section of the network

    """
    parent_section = create_downstream_sections(connected_line, None)
    parent_section = refine_sections(parent_section)
    parent_section.attach_to_lines()
    return parent_section


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
    update_direction_based_on_slack_bus(slack_bus, bus_list, line_list)

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


def update_direction_based_on_slack_bus(
    slack_bus: Bus,
    bus_list: list,
    line_list: list,
):
    """
    Update directions based on slack bus
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


def flatten(toflatten: list):
    """
    Function that flattens nested list, handy for printing

    Parameters
    ----------
    toflatten : list
        Nested list

    Returns
    -------
    None

    """
    for element in toflatten:
        try:
            yield from flatten(element)
        except TypeError:
            yield element


def find_backup_lines_between_sub_systems(
    sub_system1: SubSystem,
    sub_system2: SubSystem,
):
    """
    Finds connections between sub systems (sub_system1 and sub_system2)

    Parameters
    ----------
    sub_system1 : SubSystem
        A SubSystem element
    sub_system2 : SubSystem
        A SubSystem element

    Returns
    -------
    backup_lines : list
        List of backup lines connecting sub systems

    """

    external_backup_lines1 = find_external_backup_lines(sub_system1)
    external_backup_lines2 = find_external_backup_lines(sub_system2)
    # Extract backup lines
    backup_lines = intersection(
        external_backup_lines1,
        external_backup_lines2,
    )
    return backup_lines


def find_external_backup_lines(sub_system: SubSystem):
    """
    Finds lines connected to sub system buses that are connected to external sub systems and returns a list of external backup lines

    Parameters
    ----------
    sub_system : SubSystem
        A SubSystem element

    Returns
    -------
    external_backup_lines : list
        List containing external backup lines

    """
    external_backup_lines = list()
    for bus in sub_system.buses:
        for line in bus.connected_lines:
            if line not in sub_system.lines and line.is_backup:
                external_backup_lines.append(line)
                external_backup_lines = unique(external_backup_lines)
    return external_backup_lines
