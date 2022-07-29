from enum import Enum
from relsad.Time import Time
from relsad.network.components import Controller
from relsad.topology.ICT.dfs import is_connected


class SectionState(Enum):
    """
    Section state

    Attributes
    ----------
    CONNECTED : int
        The section is connected to its parent network
    CONNECTED : int
        The section is disconnected from its parent network
    """

    CONNECTED = 1
    DISCONNECTED = 2


class Section:

    """
    Common class for sections

    ...

    Attributes
    ----------
    lines : list
        List of lines in the section
    disconnectors : list
        List of disconnectors in the section
    parent : PowerNetwork
        The parent network for the section
    child_sections : list
        List of child sections
    state : SectionState
        The state of the section

    Methods
    ----------
    add_child_section(section)
        Adds child section to section
    attach_to_lines
        Adds lines to section and child section
    connect(dt)
        Connects the sections, connects the lines in the section and closes the disconnectors in the section
    connect_manually()
        Connects the sections, connects the lines in the section and closes the disconnectors in the section. Used when no ICT
    get_disconnect_time(dt)
        Returns the total outage time (the time the section is disconnected) of the section
    disconnect()
        Disconnects the section, the lines in the section, and opens the disconnectors in the section



    """

    __slots__ = (
        "rank",
        "lines",
        "disconnectors",
        "parent",
        "child_sections",
        "state",
    )

    def __init__(self, parent, lines, disconnectors):
        self.lines = lines
        self.disconnectors = disconnectors
        self.parent = parent
        self.child_sections = []
        self.state = SectionState.CONNECTED

    def __str__(self):
        return str(self.lines)

    def __repr__(self):
        return f"Section({str(self.lines)})"

    def __eq__(self, other):
        if hasattr(other, "lines"):
            return set(self.lines) - set(other.lines) == set()
        else:
            return False

    def __hash__(self):
        return hash(str(self.lines))

    def add_child_section(self, section):
        """
        Adds child section to section

        Parameters
        ----------
        section : Section
            A Section element

        Returns
        -------
        None

        """
        if section not in self.child_sections:
            self.child_sections.append(section)

    def attach_to_lines(self):
        """
        Adds lines to section and child section

        Parameters
        ----------
        None

        Returns
        -------
        None

        """
        for line in self.lines:
            line.section = self
        for child_section in self.child_sections:
            child_section.attach_to_lines()

    def connect(self, dt: Time, controller: Controller):
        """
        Connects the sections, connects the lines in the section and closes the disconnectors in the section

        Parameters
        ----------
        dt : Time
            The current time step
        controller : Controller
            The power network controller

        Returns
        ----------
        None

        """
        self.state = SectionState.CONNECTED
        for line in self.lines:
            line.connect()
        for discon in self.disconnectors:
            # If no ICT network
            if controller.ict_node is None:
                discon.intelligent_switch.close(dt)
            # If both components have ICT nodes
            elif (
                    controller.ict_node is not None and
                    discon.intelligent_switch.ict_node is not None
                ):
                # If the ICT nodes are connected to each other
                if is_connected(
                    node_1=controller.ict_node, 
                    node_2=discon.intelligent_switch.ict_node,
                    network=controller.ict_network,
                ):
                    discon.intelligent_switch.close(dt)
                # If the ICT nodes are not connected to each other
                else:
                    # Repair crew is assumed to be present repairing the line,
                    # they close the disconnector manually
                    discon.close()
            # If no ICT node on intelligent switch
            else:
                # Repair crew is assumed to be present repairing the line,
                # they close the disconnector manually
                discon.close()

    def connect_manually(self):
        """
        Connects the sections, connects the lines in the section and closes the disconnectors in the section. Used when no ICT

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = SectionState.CONNECTED
        for line in self.lines:
            line.connect()
        for discon in self.disconnectors:
            discon.close()

    def get_disconnect_time(self, dt: Time, controller: Controller):
        """
        Returns the total outage time (the time the section is disconnected) of the section

        Parameters
        ----------
        dt : Time
            The current time step
        controller : Controller
            The power network controller

        Returns
        ----------
        sectioning_time : Time
            The sectioning time of the section

        """
        sectioning_time = Time(0)
        need_manual_attention = False
        for discon in self.disconnectors:
            # If no ICT network
            if controller.ict_node is None:
                sectioning_time += discon.intelligent_switch.get_open_time(dt)
            # If both components have ICT nodes
            elif (
                    controller.ict_node is not None and
                    discon.intelligent_switch.ict_node is not None
                ):
                # If the ICT nodes are connected to each other
                if is_connected(
                    node_1=controller.ict_node, 
                    node_2=discon.intelligent_switch.ict_node,
                    network=controller.ict_network,
                ):
                    sectioning_time += discon.intelligent_switch.get_open_time(dt)
                # If the ICT nodes are not connected to each other
                else:
                    need_manual_attention = True
            # If no ICT node on intelligent switch
            else:
                need_manual_attention = True
        if need_manual_attention is True:
            sectioning_time += controller.manual_sectioning_time
        for line in self.lines:
            line.remaining_outage_time += sectioning_time
        return sectioning_time

    def disconnect(self):
        """
        Disconnects the section, the lines in the section, and opens the disconnectors in the section

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = SectionState.DISCONNECTED
        for line in self.lines:
            line.disconnect()
        for discon in self.disconnectors:
            discon.open()
