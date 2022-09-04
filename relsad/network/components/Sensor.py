from enum import Enum

import matplotlib.lines as mlines
import numpy as np

from relsad.Time import Time, TimeUnit
from relsad.utils import convert_yearly_fail_rate, random_choice

from .Component import Component
from .ICTNode import ICTNode
from .Line import Line


class SensorState(Enum):
    """
    Line sensor state

    Attributes
    ----------
    OK : int
        The sensor is up and running
    FAILED : int
        The sensor has failed
    REPAIR : int
        The sensor is being repaired
    """

    OK = 1
    FAILED = 2
    REPAIR = 3


class Sensor(Component):

    """
    Class defining line sensors
    ...

    Attributes
    ----------
    name : string
        Name of the sensor
    line : Line
        The line the sensor is connected to
    coordinate : list
        The coordinate of the sensor
    ict_node : ICTNode
        The ICT node connected to the sensor
    fail_rate_per_year : float
        The failure rate per year for the sensor
    p_fail_repair_new_signal : float
        The probability of a new signal can be sent
    p_fail_repair_reboot : float
        The probability that a reboot of the sensor works
    new_signal_time : Time
        The time it takes to send a new signal
    reboot_time : Time
        The time it takes to reboot the sensor
    manual_repair_time : Time
        The time it takes to manually repair the sensor
    state : SensorState
        Which state the sensor is in
    remaining_repair_time : Time
        The remaining repair time of the intelligent switch
    history : dict
        Dictonary attribute that stores the historic variables
    monte_carlo_history : dict
        Dictonary attribute that stores the historic variables from the Monte Carlo simulation

    Methods
    ----------
    fail()
        Sets the sensor state to FAILED
    not_fail()
        Sets the sensor state to OK
    draw_fail_status(dt)
        Draws the state of the sensor for a given time step
    draw_status(prob)
        Sets the state of the sensor based on the probability of the state being FAILED
    repair(dt)
        Returns the repair time and fail status of the sensor
    get_line_fail_status(dt)
        Returns the repair time and fail status of the line
    get_section()
        Returns the line section
    update_fail_status(dt)
        Updates the fail status of the sensor
        If the state of the sensor is REPAIR, the remaining repair time is set
        If the state of the sensor is OK, the state of the sensor is drawn
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_instance(random_gen)
        Adds global random instance
    print_status()
        Prints the status
    reset_status(save_flag)
        Resets the status of the sensor
    initialize_history()
        Initializes the history variables
    """

    ## Visual attributes
    color = "rosybrown"
    marker = "s"
    size = 2**2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=1,
        markersize=size,
        color=color,
        linestyle="None",
    )

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        line: Line,
        ict_node: ICTNode = None,
        fail_rate_per_year: float = 0.023,
        p_fail_repair_new_signal: float = 1 - 0.95,
        p_fail_repair_reboot: float = 1 - 0.9,
        new_signal_time: Time = Time(2, TimeUnit.SECOND),
        reboot_time: Time = Time(5, TimeUnit.MINUTE),
        manual_repair_time: Time = Time(2, TimeUnit.HOUR),
        state: SensorState = SensorState.OK,
    ):

        # Verify input
        if line is None:
            raise Exception("Sensor must be connected to a Line")
        if line.parent_network is not None:
            raise Exception(
                "Sensor must be created before the line is connected to a network"
            )
        if fail_rate_per_year < 0:
            raise Exception("The failure rate per year must be positive")
        if p_fail_repair_new_signal < 0 or p_fail_repair_new_signal > 1:
            raise Exception("p_fail_repair_new_signal must be between 0 and 1")
        if p_fail_repair_reboot < 0 or p_fail_repair_reboot > 1:
            raise Exception("p_fail_repair_reboot must be between 0 and 1")

        self.name = name
        self.line = line
        line.sensor = self

        # Define coordinate
        x1, y1 = line.fbus.coordinate
        x2, y2 = line.tbus.coordinate

        x = (x1 + x2) / 2
        y = (y1 + y2) / 2

        self.coordinate = [x, y]
        self.ict_node = ict_node
        if ict_node is not None:
            ict_node.coordinate = self.coordinate
        self.fail_rate_per_year = fail_rate_per_year
        self.p_fail_repair_new_signal = p_fail_repair_new_signal
        self.p_fail_repair_reboot = p_fail_repair_reboot
        self.new_signal_time = new_signal_time
        self.reboot_time = reboot_time
        self.remaining_repair_time = Time(0)
        self.manual_repair_time = manual_repair_time
        self.state = state

        ## History
        self.history = {}
        self.monte_carlo_history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Sensor(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Sensor)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def fail(self):
        """
        Sets the sensor state to FAILED

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = SensorState.FAILED

    def not_fail(self):
        """
        Sets the sensor state to OK

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = SensorState.OK

    def draw_fail_status(self, dt: Time):
        """
        Draws the state of the sensor for a given time step

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        p_not_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
        self.draw_status(p_not_fail)

    def draw_status(self, prob):
        """
        Sets the state of the sensor based on the probability of the state being FAILED

        Parameters
        ----------
        prob : float
            The probability that the sensor state is FAILED

        Returns
        ----------
        None

        """
        if random_choice(self.ps_random, prob):
            self.fail()
        else:
            self.not_fail()

    def repair(self, dt: Time):
        """
        Returns the repair time and fail status of the sensor

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        repair_time : Time
            The repair time of the sensor
        fail_status : bool
            The fail status of the sensor
        """
        repair_time = self.new_signal_time
        fail_status = None
        self.draw_status(self.p_fail_repair_new_signal)
        if self.state == SensorState.OK:
            fail_status = self.line.failed
            return repair_time, fail_status
        elif self.state == SensorState.FAILED:
            repair_time += self.reboot_time
            self.draw_status(self.p_fail_repair_reboot)
            if self.state == SensorState.OK:
                fail_status = self.line.failed
                return repair_time, fail_status
            elif self.state == SensorState.FAILED:
                self.remaining_repair_time = self.manual_repair_time
                self.state = SensorState.REPAIR
                fail_status = True
                return repair_time, fail_status

    def get_line_fail_status(self, dt: Time):
        """
        Returns the repair time and fail status of the line

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        repair_time : Time
            The repair time of the line
        fail_status : bool
            The fail status of the line

        """
        repair_time = None
        fail_status = None
        if self.state == SensorState.REPAIR:
            repair_time = Time(0)
            fail_status = True
            return repair_time, fail_status
        else:
            if self.state == SensorState.OK:
                repair_time = Time(0)
                fail_status = self.line.failed
                return repair_time, fail_status
            elif self.state == SensorState.FAILED:
                repair_time, fail_status = self.repair(dt)
                return repair_time, fail_status

    def get_section(self):
        """
        Returns the line section

        Parameters
        ----------
        None

        Returns
        ----------
        line_section : Section
            The parent section of the line

        """
        line_section = self.line.section
        return line_section

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status of the sensor
        If the state of the sensor is REPAIR, the remaining repair time is set
        If the state of the sensor is OK, the state of the sensor is drawn

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.state == SensorState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time <= Time(0):
                self.not_fail()
        elif self.state == SensorState.OK:
            self.draw_fail_status(dt)

    def update_history(self, prev_time, curr_time, save_flag: bool):
        """
        Updates the history variables

        Parameters
        ----------
        prev_time : Time
            The previous time
        curr_time : Time
            The current time
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["remaining_repair_time"][
                time
            ] = self.remaining_repair_time.get_unit_quantity(curr_time.unit)
            self.history["state"][time] = self.state.value

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute

        Parameters
        ----------
        attribute : str
            System attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute
        """
        return self.history[attribute]

    def add_random_instance(self, random_gen):
        """
        Adds global random instance

        Parameters
        ----------
        random_gen : np.random.default_rng()
            Random number generator

        Returns
        ----------
        None

        """
        self.ps_random = random_gen

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
        Resets the status of the sensor

        Parameters
        ----------
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        self.state = SensorState.OK
        self.remaining_repair_time = Time(0)
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
        self.history["remaining_repair_time"] = {}
        self.history["state"] = {}
