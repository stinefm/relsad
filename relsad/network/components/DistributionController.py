from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .MainController import ControllerState
from relsad.network.containers import SectionState
from relsad.utils import (
    random_choice,
    convert_yearly_fail_rate,
    unique,
)
from relsad.Time import (
    Time,
    TimeUnit,
)


class DistributionController(Component):

    """
    Common base class for disconnectors

    ...

        Attributes
        ----------
        name : string
            Name of the controller
        faile_rate : float
            The failure rate of the distribution system controller
        outage_time : float
            The outage time of the distribution system controller
        state : enum
            The state of the distribution system controller
        sectioning_time : Time
            The sectioning time of the system
        check_components : bool
        manual_sectioning_time : 
        parent_controller : 
            The parent main controller of the distribution system controller
        network : Network
            Which network the distribution system controller is connected to 
        sensors : list
            List of sensors included in the distribution system
        failed_sections : list
            List of failed sections in the distribution system
        history : dict 
            Dictonary attribute that stores the historic variables
        monte_carlo_history : dict 
            Dictonary containing the history variables from the Monte Carlo simulation

        Methods
        ----------
        check_circuitbreaker(curr_time, dt)
        disconnect_failed_sections()
            Disconnects the failed sections in the distribution system
        check_sensors(curr_time, dt)
        run_control_loop(curr_time, dt)
        check_lines_manually(curr_time)
        run_manual_control_loop(curr_time, dt)
        set_sectioning_time(sectioning_time)
            Sets the sectiom time of the distribuiton system based on the max value of the distribution sectioning time and the sectioning time set by the controller
        spread_sectioning_time_to_children()
            Gices the children network of the distribution system the same sectioning time
        update_fail_status(dt)
            Updated the fail status of the controller
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
        network,
        fail_rate: float = 0,
        outage_time: Time = Time(1, TimeUnit.HOUR),
        state: ControllerState = ControllerState.OK,
    ):

        self.name = name
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state
        self.sectioning_time = Time(0)
        self.check_components = False

        self.manual_sectioning_time = None

        self.parent_controller = None

        self.network = network

        self.sensors = []

        self.failed_sections = []

        ## History
        self.history = {}
        self.monte_carlo_history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"DistributionController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, DistributionController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def check_circuitbreaker(self, curr_time: Time, dt: Time):
        """
        Checks if the circuitbreakers in the distribution system are open. 

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
        if self.network.connected_line.circuitbreaker.is_open:
            if (
                self.sectioning_time <= Time(0)
                and not self.network.connected_line.failed
            ):
                self.disconnect_failed_sections()
                self.network.connected_line.circuitbreaker.close()
                self.network.connected_line.section.connect_manually()
                self.failed_sections = []

    def disconnect_failed_sections(self):
        """
        Disconnects the failed sections in the distribution system

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
            for x in self.network.sections
            if x.state == SectionState.CONNECTED
        ]
        disconnected_sections = [
            x
            for x in self.network.sections
            if x.state == SectionState.DISCONNECTED
        ]
        for section in disconnected_sections:
            sensors = unique([x.line.sensor for x in section.disconnectors])
            num_fails = 0
            for sensor in sensors:
                repair_time, line_fail_status = sensor.get_line_fail_status(dt)
                self.sectioning_time += repair_time
                num_fails += 1 if line_fail_status else 0
            if num_fails == 0:
                section.connect(dt)
        for section in connected_sections:
            sensors = unique([x.line.sensor for x in section.disconnectors])
            num_fails = 0
            for sensor in sensors:
                repair_time, line_fail_status = sensor.get_line_fail_status(dt)
                self.sectioning_time += repair_time
                num_fails += 1 if line_fail_status else 0
            if num_fails > 0:
                section.state = SectionState.FAILED
                self.sectioning_time += section.get_disconnect_time(dt)
                self.failed_sections.append(section)
                self.failed_sections = unique(self.failed_sections)

    def run_control_loop(self, curr_time: Time, dt: Time):
        """
        

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
            self.sectioning_time - dt if self.sectioning_time > Time(0) else Time(0)
        )
        if (
            self.network.connected_line.circuitbreaker.is_open
            and self.sectioning_time <= Time(0)
        ):
            self.check_components = True
        if self.check_components:
            self.check_sensors(curr_time, dt)
            self.spread_sectioning_time_to_children()
            self.check_components = False
        self.check_circuitbreaker(curr_time, dt)

    def check_lines_manually(self, curr_time):
        """
        

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
            for x in self.network.sections
            if x.state == SectionState.CONNECTED
        ]
        disconnected_sections = [
            x
            for x in self.network.sections
            if x.state == SectionState.DISCONNECTED
        ]
        for section in disconnected_sections:
            if sum([x.failed for x in section.lines]) == 0:
                section.connect_manually()
        for section in connected_sections:
            if sum([x.failed for x in section.lines]) > 0:
                section.state = SectionState.FAILED
                self.failed_sections.append(section)
                self.failed_sections = unique(self.failed_sections)
                self.sectioning_time = self.manual_sectioning_time
                for line in section.lines:
                    line.remaining_outage_time += self.sectioning_time

    def run_manual_control_loop(self, curr_time: Time, dt: Time):
        """
        

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
            self.sectioning_time - dt if self.sectioning_time > Time(0) else Time(0)
        )
        if (
            self.network.connected_line.circuitbreaker.is_open
            and self.sectioning_time <= Time(0)
        ):
            self.check_components = True
        if self.check_components:
            self.check_lines_manually(curr_time)
            self.spread_sectioning_time_to_children()
            self.check_components = False
        self.check_circuitbreaker(curr_time, dt)

    def set_sectioning_time(self, sectioning_time):
        """
        Sets the sectiom time of the distribuiton system based on the max value of the distribution sectioning time and the sectioning time set by the controller

        Parameters
        ----------
        sectioning_time : Time
            The sectioning time of the distribution system

        Returns
        ----------
        None

        """
        self.sectioning_time = max(
            self.sectioning_time,
            sectioning_time,
        )

    def spread_sectioning_time_to_children(self):
        """
        Gives the children network of the distribution system the same sectioning time 

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for child_network in self.network.child_network_list:
            if (
                child_network.controller.network.connected_line.circuitbreaker.is_open
            ):
                child_network.controller.set_parent_sectioning_time(
                    self.sectioning_time
                )

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status of the controller

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
            self.history["sectioning_time"][
                curr_time
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
