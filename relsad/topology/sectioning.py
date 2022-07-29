import itertools
from relsad.network.components import Line
from relsad.network.containers import Section
from relsad.utils import unique


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
        disconnectors = curr_line.disconnectors
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
            parent_section.disconnectors = parent_section.lines[0].disconnectors
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
