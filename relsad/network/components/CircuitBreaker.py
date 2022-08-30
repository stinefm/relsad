import matplotlib.lines as mlines
import numpy as np

from relsad.network.containers import SectionState
from relsad.Time import Time, TimeUnit
from relsad.utils import unique

from .Component import Component
from .Line import Line
from .Switch import Switch


class CircuitBreaker(Component, Switch):

    """
    Common base class for circuit breakers

    ...

        Attributes
        ----------
        name : string
            Name of the circuit breaker
        line : Line
            The line the circuit breaker is connected to
        is_open : bool
            Indicates if the circuit breaker is open or closed
        fail_rate : float
            The failure rate of the circuit breaker [no. of fails per year]
        outage_time : Time
            The outage time of the circuit breaker
        coordinate : list
            Coordinate of the circuit breaker
        initial_state : bool
            The initial state of the circuit breaker
        failed : bool
            True if the circuit breaker is in a failed state, False if not
        history : dict
            Dictonary attribute that stores the historic variables

        Methods
        ----------
        close()
            Closes the circuit breaker and the disconnectors connected to the host line
        open()
            Opens the circuit breaker and the disconnectors connected to the host line
        update_fail_status(dt)
            Updates the failure status of the circuit breaker
        initialize_history()
            Initializes the history variables
        update_history(prev_time, curr_time, save_flag)
            Updates the history variables
        get_history(attribute)
            Returns the history variables of an attribute
        add_random_instance(random_gen)
            Adds global random seed
        print_status()
            Prints the status
        reset_status(save_flag)
            Resets and sets the status of the system parameters


    """

    ## Visual attributes
    color = "black"
    edgecolor = "black"
    marker = "s"
    size = 3**2
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
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        line: Line,
        is_open: bool = False,
        fail_rate: float = 0.0,
        outage_time: Time = Time(1, TimeUnit.HOUR),
    ):

        # Verify input
        if line is None:
            raise Exception("CircuitBreaker must be connected to a Line")
        if line.parent_network is not None:
            raise Exception(
                "CircuitBreaker must be created before the line is connected to a network"
            )
        if fail_rate < 0:
            raise Exception("The failure rate must be positive")

        self.name = name

        dx = line.tbus.coordinate[0] - line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1] - line.fbus.coordinate[1]
        self.coordinate = [
            line.fbus.coordinate[0] + dx / 3,
            line.fbus.coordinate[1] + dy / 3,
        ]
        self.initial_state = is_open
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.line = line

        # Add this circuitbreaker to parent line
        self.line.circuitbreaker = self

        ## History
        self.history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"CircuitBreaker(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, CircuitBreaker
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def close(self):
        """
        Closes the circuit breaker and the disconnectors connected to the circuit breaker

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.is_open = False
        self.color = "black"
        for discon in self.line.disconnectors:
            if (
                discon.is_open
                and self.line.section.state == SectionState.CONNECTED
            ):
                discon.close()
        if not self.line.connected:
            self.line.connect()

    def open(self):
        """
        Opens the circuit breaker and the disconnectors connected to the circuit breaker

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.is_open = True
        self.color = "white"
        for discon in self.line.disconnectors:
            if not discon.is_open:
                discon.open()
        if self.line.connected:
            self.line.disconnect()

    def update_fail_status(self, dt: Time):
        """
        Updates the failuer status of the circuit breaker

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        pass

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
        self.history["is_open"] = {}

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
            self.history["is_open"][time] = self.is_open

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
        self.close()
        if save_flag:
            self.initialize_history()


if __name__ == "__main__":
    pass
