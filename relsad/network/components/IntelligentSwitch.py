from enum import Enum

import matplotlib.lines as mlines
import numpy as np

from relsad.Time import Time, TimeUnit
from relsad.utils import convert_yearly_fail_rate, random_choice

from .Component import Component
from .Disconnector import Disconnector
from .ICTNode import ICTNode


class IntelligentSwitchState(Enum):
    """
    Intelligent switch state

    Attributes
    ----------
    OK : int
        The intelligent switch is up and running
    FAILED : int
        The intelligent switch has failed
    REPAIR : int
        The intelligent switch is being repaired
    """

    OK = 1
    FAILED = 2
    REPAIR = 3


class IntelligentSwitch(Component):

    """
    Common class for batteries
    ...

    Attributes
    ----------
    name : string
        Name of the intelligent switch
    disconnector : Disconnector
        The disconnector the intelligent switch is connected to
    ict_node : ICTNode
        The ICT node connected to the intelligent switch
    fail_rate_per_year : float
        The failure rate per year for the intelligent switch
    manual_repair_time : Time
        The time it takes to manually repair the intelligent switch
    state : IntelligentSwitchState
        Which state the intelligent switch is in
    remaining_repair_time : Time
        The remaining repair time of the intelligent switch
    history : dict
        Dictonary attribute that stores the historic variables
    monte_carlo_history : dict
        Dictonary attribute that stores the historic variables from the Monte Carlo simulation

    Methods
    ----------
    fail()
        Sets the intelligent switch state to FAILED
    not_fail()
        Sets the intelligent switch state to OK
    draw_fail_status(dt)
        Draws the state of the intelligent switch for a given time step
    draw_status(prob)
        Sets the state of the intelligent switch based on the probability of the state being FAILED
    get_open_repair_time(dt)
        Returns the time it takes to open the intelligent switch when it must be repaired
    get_open_time(dt)
        Returns the time it takes to open the intelligent switch based on the status
    open()
        Opens the disconnector
    repair_close(dt)
        Sets the remaining repair time of the intelligent switch
        Closes the disconnector
        Sets the state of the intelligent switch to repair
    close(dt)
        Closes the disconnector if the state of the intelligent switch is OK
    update_fail_status(dt)
        Updates the fail status of the intelligent switch
        If the state of the intelligent switch is REPAIR, the remaining repair time is calculated
        If the state of the intelligent switch is OK, the state of the intelligent switch is drawn
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_instance(random_gen)
        Adds global random instance
    print_status()
        Prints the status
    reset_status(save_flag)
        Resets the status of the intelligent switch
    initialize_history()
        Initializes the history variables
    """

    ## Visual attributes
    color = "seagreen"
    marker = "x"
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
        disconnector: Disconnector,
        ict_node: ICTNode = None,
        fail_rate_per_year: float = 0.03,
        manual_repair_time: Time = Time(2, TimeUnit.HOUR),
        state: IntelligentSwitchState = IntelligentSwitchState.OK,
    ):

        # Verify input
        if disconnector is None:
            raise Exception(
                "IntelligentSwitch must be connected to a Disconnector"
            )
        if fail_rate_per_year < 0:
            raise Exception("The failure rate per year must be positive")

        self.name = name
        self.disconnector = disconnector
        disconnector.intelligent_switch = self
        self.ict_node = ict_node
        if ict_node is not None:
            ict_node.coordinate = self.disconnector.coordinate
        self.fail_rate_per_year = fail_rate_per_year
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
        return f"IntelligentSwitch(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, IntelligentSwitch
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def fail(self):
        """
        Sets the intelligent switch state to FAILED

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = IntelligentSwitchState.FAILED

    def not_fail(self):
        """
        Sets the intelligent switch state to OK

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.state = IntelligentSwitchState.OK

    def draw_fail_status(self, dt: Time):
        """
        Draws the state of the intelligent switch for a given time step

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
        self.draw_status(p_fail)

    def draw_status(self, prob):
        """
        Sets the state of the intelligent switch based on the probability of the state being FAILED

        Parameters
        ----------
        prob : float
            The probability that the intelligent switch state is FAILED

        Returns
        ----------
        None

        """
        if random_choice(self.ps_random, prob):
            self.fail()
        else:
            self.not_fail()

    def get_open_repair_time(self, dt: Time):
        """
        Returns the time it takes to open the intelligent switch
        when it must be repaired

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        open_repair_time: Time
            The time it takes to open the intelligent switch
            when it must be repaired

        """
        self.remaining_repair_time = self.manual_repair_time
        self.state = IntelligentSwitchState.REPAIR
        open_repair_time = (
            self.disconnector.line.parent_network.controller.manual_sectioning_time
        )
        return open_repair_time

    def get_open_time(self, dt: Time):
        """
        Returns the time it takes to open the intelligent switch
        based on the status

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        open_time: Time
            The time it takes to open the intelligent switch
            based on the status

        """
        open_time = None
        if self.state == IntelligentSwitchState.REPAIR:
            open_time = Time(0)
        else:
            if self.state == IntelligentSwitchState.OK:
                open_time = Time(0)
            elif self.state == IntelligentSwitchState.FAILED:
                open_time = self.get_open_repair_time(dt)
        return open_time

    def open(self):
        """
        Opens the disconnector

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.disconnector.open()

    def repair_close(self, dt: Time):
        """
        Sets the remaining repair time of the intelligent switch
        Closes the disconnector
        Sets the state of the intelligent switch to repair

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        # Repair is started
        self.remaining_repair_time = self.manual_repair_time
        # Repair crew is assumed to be present repairing the line,
        # they close the disconnector manually
        self.disconnector.close()
        self.state = IntelligentSwitchState.REPAIR

    def close(self, dt: Time):
        """
        Closes the disconnector if the state of the intelligent switch is OK


        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if not self.state == IntelligentSwitchState.REPAIR:
            if self.state == IntelligentSwitchState.OK:
                self.disconnector.close()
            elif self.state == IntelligentSwitchState.FAILED:
                self.repair_close(dt)

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status of the intelligent switch
        If the state of the intelligent switch is REPAIR, the remaining repair time is calculated
        If the state of the intelligent switch is OK, the state of the intelligent switch is drawn

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.state == IntelligentSwitchState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time <= Time(0):
                self.not_fail()
        elif self.state == IntelligentSwitchState.OK:
            self.draw_fail_status(dt)

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
        Resets the status of the intelligent switch

        Parameters
        ----------
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        self.state = IntelligentSwitchState.OK
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
