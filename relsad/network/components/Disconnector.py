import matplotlib.lines as mlines
import numpy as np

from relsad.Time import Time, TimeUnit

from .Bus import Bus
from .Component import Component
from .Line import Line
from .Switch import Switch


class Disconnector(Component, Switch):

    """
    Common base class for disconnectors

    ...

        Attributes
        ----------
        name : string
            Name of the disconnector
        coordinate : list
            The coordinate of the disconnector
        initial_state : bool
            The initial state of the disconnector (open or colsed)
        is_open : bool
            Tells if the switch is open (True) or closed (False)
        failed : bool
            True if the disconnector is in a failed state, False if not
        fail_rate : float
            The failure rate of the disconnector [no. of fails per year]
        outage_time : Time
            The outage time of the diconnector
        prev_open_time : Time
            The time of the previous time step
        line : Line
            The line the disconnecor is connected to
        base_bus : Bus
            Wich bus the disconnector is closes to (for setting coordinates)
        intelligent_switch : IntelligentSwitch
            Returns the intelligent switch connected to the disconnector if any
        history : dict
            Dictonary attribute that stores the historic variables

        Methods
        ----------
        close()
            Closes the disconnector
        open()
            Opens the disconnector
        fail()
            Sets the disconnector to failed and opens the disconnector
        not_fail()
            Sets the doconnector to not failed and closes the disconnector
        initialize_history()
            Initializes the history variables
        update_history(prev_time, curr_time, save_flag)
            Updates the history variables
        get_history(attribute)
            Returns the history variables of an attribute
        add_random_instance(random_gen)
            Adds global random seed
        reset_status(save_falg)
            Resets and sets the status of the system parameters

    """

    ## Visual attributes
    color = "black"
    edgecolor = "black"
    marker = "o"
    size = 2**2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=2,
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
        bus: Bus,
        is_open: bool = False,
        fail_rate: float = 0.014,
        outage_time: Time = Time(1, TimeUnit.HOUR),
    ):

        # Verify input
        if line is None:
            raise Exception("Disconnector must be connected to a Line")
        if line.parent_network is not None:
            raise Exception(
                "Disconnector must be created before the line is connected to a network"
            )
        if bus is None:
            raise Exception("Disconnector must be connected to a Bus")
        if bus not in [line.fbus, line.tbus]:
            raise Exception(
                "Disconnector must be connected to a base bus connected "
                "to the line it is located on"
            )
        if fail_rate < 0:
            raise Exception("The failure rate must be positive")

        self.name = name
        self.initial_state = is_open
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.prev_open_time = Time(0)
        self.line = line

        ## Set coordinate
        self.base_bus = bus
        dx = line.tbus.coordinate[0] - line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1] - line.fbus.coordinate[1]
        if bus == line.tbus:
            dx *= -1
            dy *= -1

        line.disconnectors.append(self)
        self.coordinate = [
            self.base_bus.coordinate[0] + dx / 4,
            self.base_bus.coordinate[1] + dy / 4,
        ]

        ## Communication
        self.intelligent_switch = None

        ## History
        self.history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Disconnector(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Disconnector)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def close(self):
        """
        Closes the disconnector

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.is_open = False
        self.color = "black"
        if not self.line.connected:
            self.line.connect()

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
        self.is_open = True
        self.color = "white"
        if self.line.connected:
            self.line.disconnect()

    def fail(self):
        """
        Sets the disconnecotr to failed and opens the disconnector

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.failed = True
        self.open()

    def not_fail(self):
        """
        Sets the disconnector to not failed and closes the disconnecotr

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.failed = False
        self.close()

    def update_fail_status(self, dt: Time):
        """

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """

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

        Parameters
        ----------

        Returns
        ----------
        None

        """

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

        self.not_fail()
        if save_flag:
            self.initialize_history()


if __name__ == "__main__":
    pass
