import matplotlib.lines as mlines
import numpy as np

from relsad.StatDist import StatDist, StatDistType, UniformParameters
from relsad.Time import Time, TimeUnit
from relsad.utils import convert_yearly_fail_rate, random_choice

from .Component import Component
from .ICTNode import ICTNode


class ICTLine(Component):
    r"""
    A class used to represent an ICT Line

    ...

    Attributes
    ----------
    name : str
        Name of the line
    fnode : ICTNode
        Sending ICT node
    tnode : ICTNode
        Receiving ICT node
    parent_network : ICTNetwork
        The parent ICT network of the line
    fail_rate_per_year : float
        Failure rate per year [fault/year/km]
    repair_time_dist : StatDist
        The repair time of the line [hours/fault]
    connected : bool
        Indicates if the line is connected or disconnected
    failed : bool
        Failure status of the line
    remaining_outage_time : Time
        The remaining outage time of the line
    history : dict
        Dictonary attribute that stores the historic variables


    Methods
    -------
    disconnect()
        Disconnects a line and removes the line for the list of lines
    connect()
        Connects a line and append the line to the list of lines
    draw_repair_time(dt)
        Decides and returns the repair time of the line based on a statistical distribution
    fail(dt)
        Sets the fail status of the line to True and opens the connected disconnectors and the connected circuit breaker
    not_fail()
        Sets the fail status of the line to False and closes the connected disconnectors and connected circuit breaker
    change_direction()
        Changes the direction of the line
    update_fail_status(dt)
        Updates the fail status of the line
    print_status()
        Prints the line status
    add_parent_network(network)
        Adds the parent network to the line
    initialize_history()
        Initialize the history variables
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_instance(random_gen)
        Adds global random seed
    reset_status()
        Resets and sets the status of the class parameters
    """
    lineCount = 0

    ## Visual attributes
    linestyle = "dotted"
    handle = mlines.Line2D([], [], linestyle=linestyle)

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        fnode: ICTNode,
        tnode: ICTNode,
        repair_time_dist: StatDist = StatDist(
            stat_dist_type=StatDistType.UNIFORM_FLOAT,
            parameters=UniformParameters(
                min_val=0.0,
                max_val=0.0,
            ),
        ),
        fail_rate_per_year: float = 0.0,  # fails/year
        connected=True,
    ):

        # Verify input
        if fnode is None:
            raise Exception("Line must have a origin ICT node")
        if tnode is None:
            raise Exception("Line must have a target ICT node")
        if repair_time_dist is None:
            raise Exception("The line must have a repair time distribution")
        if fail_rate_per_year < 0:
            raise Exception("The failure rate per year must be positive")

        ## Informative attributes
        self.name = name

        ## Topological attributes
        self.fnode = fnode
        self.tnode = tnode
        fnode.connected_lines.append(self)
        tnode.connected_lines.append(self)
        tnode.toline = self
        tnode.toline_list.append(self)
        fnode.fromline = self
        fnode.fromline_list.append(self)
        self.parent_network = None
        ICTLine.lineCount += 1

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_per_year
        self.repair_time_dist = repair_time_dist

        ## Status attribute
        self.connected = connected
        self.failed = False
        self.remaining_outage_time = Time(0)

        ## History
        self.history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ICTLine(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, ICTLine)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def disconnect(self):
        """
        Disconnects a line and removes the line from the list of lines

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.connected:
            self.connected = False
            self.linestyle = "--"
            self.fnode.fromline_list.remove(self)
            if self.fnode.fromline == self:
                if len(self.fnode.fromline_list) > 0:
                    self.fnode.fromline = next(iter(self.fnode.fromline_list))
                else:
                    self.fnode.fromline = None
            self.tnode.toline_list.remove(self)
            if self.tnode.toline == self:
                if len(self.tnode.toline_list) > 0:
                    self.tnode.toline = next(iter(self.tnode.toline_list))
                else:
                    self.tnode.toline = None

    def connect(self):
        """
        Connects a line and append the line to the list of lines

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if not self.connected:
            self.connected = True
            self.linestyle = "-"
            self.tnode.toline = self
            self.tnode.toline_list.append(self)
            self.fnode.fromline = self
            self.fnode.fromline_list.append(self)

    def draw_repair_time(self, dt: Time):
        """
        Decides and returns the repair time of the line based on a statistical distribution

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        return Time(
            self.repair_time_dist.draw(
                random_instance=self.ps_random,
                size=1,
            )[0],
            dt.unit,
        )

    def fail(self, dt: Time):
        """
        Sets the fail status of the line to False

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        self.failed = True
        self.parent_network.failed_line = True
        self.remaining_outage_time = self.draw_repair_time(dt)

    def not_fail(self):
        """
        Sets the fail status of the line to False

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if (
            sum([line.failed for line in self.parent_network.lines]) == 1
            and self.failed
        ):
            self.parent_network.failed_line = False
        self.failed = False

    def change_direction(self):
        """
        Changes the direction of the line

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.fnode.fromline_list.remove(self)
        self.tnode.fromline_list.append(self)
        self.tnode.toline_list.remove(self)
        self.fnode.toline_list.append(self)
        if self.fnode.fromline == self:
            self.fnode.fromline = (
                next(iter(self.fnode.fromline_list))
                if len(self.fnode.fromline_list) > 0
                else None
            )
        if self.tnode.toline == self:
            self.tnode.toline = (
                next(iter(self.tnode.toline_list))
                if len(self.tnode.toline_list) > 0
                else None
            )
        self.fnode.toline = self
        self.tnode.fromline = self
        node = self.fnode
        self.fnode = self.tnode
        self.tnode = node

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status of the line

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        if self.failed:
            self.remaining_outage_time -= dt
            if self.remaining_outage_time <= Time(0):
                self.not_fail()
                self.remaining_outage_time = Time(0)
        else:
            p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
            if random_choice(self.ps_random, p_fail):
                self.fail(dt)
            else:
                self.not_fail()

    def print_status(self):
        """
        Prints the line status

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        print(
            "name: {:5s}, failed={}, connected={}".format(
                self.name, self.failed, self.connected
            )
        )

    def add_parent_network(self, network):
        """
        Adds the parent network to the line

        Parameters
        ----------
        network : PowerNetwork
            The parent network of the line

        Returns
        ----------
        None

        """

        self.parent_network = network

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
        self.history["remaining_outage_time"] = {}
        self.history["failed"] = {}

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
            The vurrent time
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["remaining_outage_time"][
                time
            ] = self.remaining_outage_time.get_unit_quantity(curr_time.unit)
            self.history["failed"][time] = self.failed

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
        self.remaining_outage_time = Time(0)

        self.not_fail()
        if save_flag:
            self.initialize_history()


if __name__ == "__main__":
    pass
