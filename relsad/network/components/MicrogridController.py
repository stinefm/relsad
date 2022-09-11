from enum import Enum

import matplotlib.lines as mlines
import numpy as np

from relsad.network.containers import SectionState
from relsad.Time import Time, TimeUnit
from relsad.topology.ICT.dfs import is_connected
from relsad.utils import convert_yearly_fail_rate, random_choice, unique

from .Component import Component
from .Controller import Controller, ControllerState
from .ICTNode import ICTNode


class MicrogridMode(Enum):
    """
    Microgrid mode

    Attributes
    ----------
    SURVIVAL : int
        The microgrid is in survival mode, it disconnects
        from the parent power network for the entire failure
        duration
    FULL_SUPPORT : int
        The microgrid is in full support mode, it disconnects
        from the parent power network only during sectioning time.
        When connected to the parent power network, the microgrid
        provides all the support it has available.
    LIMITED_SUPPORT : int
        The microgrid is in limited support mode, it disconnects
        from the parent power network only during sectioning time.
        When connected to the parent power network, the microgrid
        provides only surplus support.
    """

    SURVIVAL = 1
    FULL_SUPPORT = 2
    LIMITED_SUPPORT = 3


class MicrogridController(Component, Controller):
    """
    Common class for microgrid controller

    ...

    Attributes
    ----------
    name : string
        Name of the microgird controller
    ict_node : ICTNode
        The ICT node connected to the controller
    fail_rate : float
        The failure rate of the microgrid controller
    outage_time : float
        The outage time of the microgrid controller
    state : ControllerState
        The state of the microgrid controller
    sectioning_time : Time
        The sectioning time in the microgrid
    parent_sectioning_time : Time
        The sectioning time of the parent controller
    check_components : bool
    manual_sectioning_time : Time
        The sectioning time of a passive microgrid without
        controller (or controller is failed)
    power_network : PowerNetwork
        The power network the controller belongs to
    ict_network : ICTNetwork
        The ICT network the controller belongs to
    sensors : list
        List of sensors associated with the microgrid
    failed_sections : list
        List of failed sections in the microgrid
    history : dict
        Dictonary attribute that stores the historic variables
    monte_carlo_history : dict


    Methods
    ----------
    check_circuitbreaker(curr_time, dt)
        Checks if the circuitbreaker in the distribution system is open.
        If sectioning time is finished, disconnect failed sections and close the
        circuitbreaker.
    check_circuitbreaker_manually(curr_time, dt)
        Checks if the circuitbreaker in the distribution system is open manually.
        If sectioning time is finished, disconnect failed sections and close the
        circuitbreaker.
    disconnect_failed_sections()
        Disconnects the failed sections in the microgrid
    check_sensors(curr_time, dt)
        Loops through the sections connected to the controller determining which
        sensors have failed. Performs actions according to the sensor status
        in the respective section.
        If a section was disconnected and no longer includes any failed sensor,
        it is connected.
        If a section was connected and now includes a failed sensor, it is disconnected.
        The total sectioning time is summed from each section.
    run_control_loop(curr_time, dt)
        System control check, determines if components have failed and performes
        the required action
    check_lines_manually(curr_time)
        Loops manually through the sections connected to the controller determining
        which lines have failed. Performs actions according
        to the line status in the respective section.

        If a section was disconnected and no longer includes any failed
        lines, it is connected.

        If a section was connected and now includes a failed line,
        it is disconnected.

        The total sectioning time is summed from each section.
    run_manual_control_loop(curr_time, dt)
        Manual system control check, determines if components have failed and
        performes the required action.
    set_sectioning_time(sectioning_time)
        Sets the sectiom time of the microgrid based on the max value
        of the microgrid sectioning time and the sectioning time set by the
        controller
    set_parent_sectioning_time(sectioning_time)
        Sets the sectioning time of the parent power network
    update_fail_status(dt)
        Updates the fail status
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_instance(random_gen)
        Adds global random seed
    print_status()
        Prints the status
    reset_status(save_flag)
        Resets and sets the status of the class parameters
    initialize_history()
        Initializes the history variables
    """

    def __init__(
        self,
        name: str,
        power_network,
        fail_rate: float = 0,
        outage_time: Time = Time(1, TimeUnit.HOUR),
        state: ControllerState = ControllerState.OK,
    ):

        self.name = name
        self.ict_node = None
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state
        self.sectioning_time = Time(0)
        self.parent_sectioning_time = Time(0)
        self.check_components = False

        self.manual_sectioning_time = None

        self.power_network = power_network
        self.ict_network = None

        self.sensors = []

        self.failed_sections = []

        ## History
        self.history = {}
        self.monte_carlo_history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"MicrogridController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, MicrogridController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def check_circuitbreaker(self, curr_time: Time, dt: Time):
        """
        Checks if the circuitbreaker in the distribution system is open.
        If sectioning time is finished, disconnect failed sections and close the
        circuitbreaker.

        Parameters
        ----------
        curr_time : Time
            The current time
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.power_network.connected_line.circuitbreaker.is_open:
            # If circuitbreaker in Microgrid with survival mode and parent Distribution
            # system has no failed lines
            if (
                self.power_network.mode == MicrogridMode.SURVIVAL
                and self.power_network.distribution_network.failed_line is True
            ):
                return
            elif self.sectioning_time <= Time(0):
                self.disconnect_failed_sections()
                if (
                    not self.power_network.connected_line.failed
                    and self.power_network.connected_line
                    not in [
                        line
                        for section in self.failed_sections
                        for line in section.lines
                    ]
                ):
                    # Sectioning time finished
                    self.power_network.connected_line.circuitbreaker.close()
                    self.power_network.connected_line.section.connect(dt, self)
                    self.failed_sections = []

    def check_circuitbreaker_manually(self, curr_time: Time, dt: Time):
        """
        Checks if the circuitbreaker in the distribution system is open manually.
        If sectioning time is finished, disconnect failed sections and close the
        circuitbreaker.

        Parameters
        ----------
        curr_time : Time
            The current time
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.power_network.connected_line.circuitbreaker.is_open:
            # If circuitbreaker in Microgrid with survival mode and parent Distribution
            # system has no failed lines
            if (
                self.power_network.mode == MicrogridMode.SURVIVAL
                and self.power_network.distribution_network.failed_line is True
            ):
                return
            elif self.sectioning_time <= Time(0):
                self.disconnect_failed_sections()
                if not self.power_network.connected_line.failed:
                    # Sectioning time finished
                    self.power_network.connected_line.circuitbreaker.close()
                    self.power_network.connected_line.section.connect_manually()
                    self.failed_sections = []

    def disconnect_failed_sections(self):
        """
        Disconnects the failed sections in the microgrid

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for section in self.failed_sections:
            section.disconnect()

    def check_sensors(self, curr_time: Time, dt: Time):
        """
        Loops through the sections connected to the controller determining which
        sensors have failed. Performs actions according to the sensor status
        in the respective section.
        If a section was disconnected and no longer includes any failed sensor,
        it is connected.
        If a section was connected and now includes a failed sensor, it is disconnected.
        The total sectioning time is summed from each section.

        Parameters
        ----------
        curr_time : Time
            The current time
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        connected_sections = [
            x
            for x in self.power_network.sections
            if x.state == SectionState.CONNECTED
        ]
        disconnected_sections = [
            x
            for x in self.power_network.sections
            if x.state == SectionState.DISCONNECTED
        ]
        for section in disconnected_sections:
            sensors = unique(
                [
                    switch.line.sensor
                    for switch in section.switches
                    if switch.line.sensor is not None
                ]
            )
            num_fails = 0
            need_manual_attention = False
            for sensor in sensors:
                # If no ICT network
                if self.ict_node is None:
                    (
                        repair_time,
                        line_fail_status,
                    ) = sensor.get_line_fail_status(dt)
                    self.sectioning_time += repair_time
                # If both components have ICT nodes
                elif self.ict_node is not None and sensor.ict_node is not None:
                    # If the ICT nodes are connected to each other
                    if is_connected(
                        node_1=self.ict_node,
                        node_2=sensor.ict_node,
                        network=self.ict_network,
                    ):
                        (
                            repair_time,
                            line_fail_status,
                        ) = sensor.get_line_fail_status(dt)
                        self.sectioning_time += repair_time
                    # If the ICT nodes are not connected to each other
                    else:
                        need_manual_attention = True
                        line_fail_status = sensor.line.failed
                # If no ICT node on sensor
                else:
                    need_manual_attention = True
                    line_fail_status = sensor.line.failed
                num_fails += 1 if line_fail_status else 0
            if need_manual_attention is True:
                self.sectioning_time += self.manual_sectioning_time
            if num_fails == 0:
                section.connect(dt, self)
                if section in self.failed_sections:
                    self.failed_sections.remove(section)
        # Loop connected sections
        for section in connected_sections:
            sensors = unique(
                [
                    switch.line.sensor
                    for switch in section.switches
                    if switch.line.sensor is not None
                ]
            )
            num_fails = 0
            need_manual_attention = False
            # Loop sensors and count failed ones
            for sensor in sensors:
                # If no ICT network
                if self.ict_node is None:
                    (
                        repair_time,
                        line_fail_status,
                    ) = sensor.get_line_fail_status(dt)
                    self.sectioning_time += repair_time
                # If both components have ICT nodes
                elif self.ict_node is not None and sensor.ict_node is not None:
                    # If the ICT nodes are connected to each other
                    if is_connected(
                        node_1=self.ict_node,
                        node_2=sensor.ict_node,
                        network=self.ict_network,
                    ):
                        (
                            repair_time,
                            line_fail_status,
                        ) = sensor.get_line_fail_status(dt)
                        self.sectioning_time += repair_time
                    # If the ICT nodes are not connected to each other
                    else:
                        need_manual_attention = True
                        line_fail_status = sensor.line.failed
                # If no ICT node on sensor
                else:
                    need_manual_attention = True
                    line_fail_status = sensor.line.failed
                num_fails += 1 if line_fail_status else 0
            if need_manual_attention is True:
                self.sectioning_time += self.manual_sectioning_time
            if num_fails > 0:
                section.state = SectionState.DISCONNECTED
                self.sectioning_time += section.get_disconnect_time(dt, self)
                self.failed_sections.append(section)
                self.failed_sections = unique(self.failed_sections)

    def run_control_loop(self, curr_time: Time, dt: Time):
        """
        System control check, determines if components have failed and performes
        the required action

        Parameters
        ----------
        curr_time : Time
            The current time
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        self.sectioning_time = (
            self.sectioning_time - dt
            if self.sectioning_time > Time(0)
            else Time(0)
        )
        self.sectioning_time = max(
            self.sectioning_time,
            self.parent_sectioning_time,
        )
        if (
            self.power_network.connected_line.circuitbreaker.is_open
            and self.sectioning_time <= Time(0)
        ):
            self.check_components = True
        if self.check_components:
            self.check_sensors(curr_time, dt)
            self.check_components = False
        self.check_circuitbreaker(curr_time, dt)

    def check_lines_manually(self, curr_time):
        """
        Loops manually through the sections connected to the controller determining
        which lines have failed. Performs actions according
        to the line status in the respective section.

        If a section was disconnected and no longer includes any failed
        lines, it is connected.

        If a section was connected and now includes a failed line,
        it is disconnected.

        The total sectioning time is summed from each section.

        Parameters
        ----------
        curr_time : Time
            The current time

        Returns
        ----------
        None

        """
        connected_sections = [
            x
            for x in self.power_network.sections
            if x.state == SectionState.CONNECTED
        ]
        disconnected_sections = [
            x
            for x in self.power_network.sections
            if x.state == SectionState.DISCONNECTED
        ]
        # Loop disconnected sections
        for section in disconnected_sections:
            if sum([x.failed for x in section.lines]) == 0:
                section.connect_manually()
                if section in self.failed_sections:
                    self.failed_sections.remove(section)
        # Loop connected sections
        for section in connected_sections:
            if sum([x.failed for x in section.lines]) > 0:
                section.state = SectionState.DISCONNECTED
                self.failed_sections.append(section)
                self.failed_sections = unique(self.failed_sections)
                self.sectioning_time = self.manual_sectioning_time
                for line in section.lines:
                    line.remaining_outage_time += self.sectioning_time

    def run_manual_control_loop(self, curr_time: Time, dt: Time):
        """
        Manual system control check, determines if components have failed and
        performes the required action.

        Parameters
        ----------
        curr_time : Time
            The current time
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        self.sectioning_time = (
            self.sectioning_time - dt
            if self.sectioning_time > Time(0)
            else Time(0)
        )
        self.sectioning_time = max(
            self.sectioning_time,
            self.parent_sectioning_time,
        )
        if (
            self.power_network.connected_line.circuitbreaker.is_open
            and self.sectioning_time <= Time(0)
        ):
            self.check_components = True
        if self.check_components:
            self.check_lines_manually(curr_time)
            self.check_components = False
        self.check_circuitbreaker_manually(curr_time, dt)

    def set_sectioning_time(self, sectioning_time):
        """
        Sets the sectiom time of the microgrid based on the max value
        of the microgrid sectioning time and the sectioning time set by the
        controller

        Parameters
        ----------
        sectioning_time : Time
            The sectioning time in the microgrid

        Returns
        ----------
        None

        """
        self.sectioning_time = max(
            self.sectioning_time,
            sectioning_time,
        )

    def set_parent_sectioning_time(self, sectioning_time):
        """
        Sets the sectioning time of the parent power network

        Parameters
        ----------
        sectioning_time : Time
            The sectioning time in the microgrid

        Returns
        ----------
        None

        """
        self.parent_sectioning_time = sectioning_time

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        pass

    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        """
        Updates the history variables

        Parameters
        ----------
        prev_time : Time
            The previous time
        curr_time : Time
            Current time
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["sectioning_time"][
                time
            ] = self.sectioning_time.get_unit_quantity(curr_time.unit)

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute

        Parameters
        ----------
        attribute : str
            Controller attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def add_random_instance(self, random_gen):
        """
        Adds global random seed

        Parameters
        ----------
        random_gen : int
            Random number generator

        Returns
        ----------
        None

        """
        pass

    def print_status(self):
        """
        Prints the status

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        pass

    def reset_status(self, save_flag: bool):
        """
        Resets and sets the status of the class parameters

        Parameters
        ----------
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        self.prev_open_time = Time(0)
        self.sectioning_time = Time(0)
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        """
        Initializes the history variables

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.history["sectioning_time"] = {}
