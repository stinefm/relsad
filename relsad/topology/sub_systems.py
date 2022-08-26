import itertools

from relsad.network.systems import SubSystem
from relsad.utils import intersection, unique


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
