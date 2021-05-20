from .Component import Component
from .Line import Line
from .Bus import Bus
from .Circuitbreaker import CircuitBreaker
import matplotlib.lines as mlines
import numpy as np


class Disconnector(Component):

    """
    Common base class for disconnectors

    ...

        Attributes
        ----------
        name : string
            Name of the disconnector
        initial_state : book
            The initial state of the disconnector
        is_open : bool
            Tells if the switch is open (True) or closed (False)
        failed : bool
            True if the disconnector is in a failed state, False if not
        fail_rate : float
            The failure rate of the disconnector [no of fails per year]
        outage_time : float
            The outage time of the diconnector [time units]
        prev_open_time : float
            The time for the previous time step
        line : Line
            The line the disconnecor is connected to
        base_bus : Bus
            Wich bus the disconnector is closes to (for setting coordinates)
        history : dict
            Dictonary attribute that stores the historic variables

        Methods
        ----------
        close(curr_time)
            Closes the disconnector
        open(curr_time)
            Opens the disconnector
        fail(curr_time)
            Sets the diconnecotr to failed
        not_fail(curr_time)
            Sets the doconnector to not failed
        update_fail_status(curr_time)
        update_history(curr_time)
            Updates the history variables
        get_history(attribute)
            Returns the history variables of an attribute
        add_random_seed(random_gen)
            Adds global random
        print_status()
        reset_status()
            Resets and sets the status of the system parameters

    """

    ## Visual attributes
    color = "black"
    edgecolor = "black"
    marker = "o"
    size = 2 ** 2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=3,
        markersize=size,
        linestyle="None",
        color=color,
        markeredgecolor=edgecolor,
    )

    ## Random instance
    ps_random = None

    def __init__(
        self,
        name: str,
        line: Line,
        bus: Bus,
        circuitbreaker: CircuitBreaker = None,
        is_open: bool = False,
        fail_rate: float = 0.014,
        outage_time: float = 1,
    ):
        self.name = name
        self.initial_state = is_open
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.prev_open_time = 0
        self.line = line
        self.circuitbreaker = circuitbreaker

        ## Set coordinate
        self.base_bus = bus
        dx = line.tbus.coordinate[0] - line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1] - line.fbus.coordinate[1]
        if bus == line.tbus:
            dx *= -1
            dy *= -1
        if self.circuitbreaker is None:
            line.disconnectors.append(self)
            self.coordinate = [
                self.base_bus.coordinate[0] + dx / 4,
                self.base_bus.coordinate[1] + dy / 4,
            ]
        else:
            self.circuitbreaker.disconnectors.append(self)
            # line.disconnectors.append(self)
            self.coordinate = [
                circuitbreaker.coordinate[0] - dx / 10,
                circuitbreaker.coordinate[1] - dy / 10,
            ]

        ## History
        self.history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Disconnector(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def close(self, curr_time):
        """
        Closes the disconnector

        Parameters
        ----------
        curr_time : int
            Current time

        Returns
        ----------
        None

        """
        if (
            curr_time > self.prev_open_time
            or self.line.is_backup
            or curr_time == 0
        ):
            self.is_open = False
            self.color = "black"
            if not self.line.connected:
                self.line.connect()

    def open(self, curr_time):
        """
        Opens the disconnector

        Parameters
        ----------
        curr_time : int
            Current time

        Returns
        ----------
        None

        """
        self.is_open = True
        self.prev_open_time = curr_time
        self.color = "white"
        if self.line.connected:
            self.line.disconnect()

    def fail(self, curr_time):
        """
        Sets the diconnecotr to failed

        Parameters
        ----------
        curr_time : int
            Current time

        Returns
        ----------
        None

        """
        self.failed = True
        self.open(curr_time)

    def not_fail(self, curr_time):
        """
        Sets the doconnector to not failed

        Parameters
        ----------
        curr_time : int
            Current time

        Returns
        ----------
        None

        """
        self.failed = False
        self.close(curr_time)

    def update_fail_status(self, curr_time):
        """

        Parameters
        ----------
        curr_time : int
            Current time

        Returns
        ----------
        None

        """
        pass

    def initialize_history(self):
        self.history["is_open"] = {}

    def update_history(self, curr_time, save_flag: bool):
        """
        Updates the history variables

        Parameters
        ----------
        curr_time : int
            Current time

        Returns
        ----------
        None

        """
        if save_flag:
            self.history["is_open"][curr_time] = self.is_open

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

    def add_random_seed(self, random_gen):
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
        self.ps_random = random_gen

    def print_status(self):
        """

        Parameters
        ----------

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
        None

        Returns
        ----------
        None

        """
        self.prev_open_time = 0

        self.not_fail(0)
        if save_flag:
            self.initialize_history()


if __name__ == "__main__":
    pass
