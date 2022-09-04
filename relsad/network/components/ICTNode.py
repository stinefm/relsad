import matplotlib.lines as mlines
import numpy as np

from relsad.StatDist import StatDist, StatDistType, UniformParameters
from relsad.utils import convert_yearly_fail_rate, random_choice
from relsad.Time import Time

from .Component import Component


class ICTNode(Component):
    """
    Common base class for all ICT nodes

    ...

    Attributes
    ----------
    name : string
        Name of the ICT node
    coordinate : list
        Coordinate of the ICT node
    toline : Line
        Tells which line that is going into the ICT node
    fromline : Line
        Tells which line that is going out of the ICT node
    toline_list : list
        List of lines going into the ICT node
    fromline_list : list
        List of lines going from the ICT node
    connected_lines : List
        List of connected lines
    parent_network : ICTNetwork
        Parent ICT network of the ICT node
    fail_rate_per_year : float
        The failure rate per year for the transformer at the ICT node
    repair_time_dist : StatDist
        The repair time of the transformer at the ICT node [hours/fault]
    remaining_outage_time : Time
        The remaining outage time of the ICT node
    acc_outage_time : Time
        The accumulated outage time of the transformer at the ICT node
    avg_outage_time : Time
        The average outage time of the transformer at the ICT node
    avg_fail_rate : float
        The average failure rate of the transformer at the ICT node
    num_consecutive_interruptions : float
        Number of consecutive interruptions a ICT node experiences
    interruption_fraction : float
        The interruption fraction of the ICT node
    acc_interruptions : float
        Accumulated interruption duration a ICT node experiences
    history : dict
        Dictonary attribute that stores the historic variables
    monte_carlo_history : dict
        Dictonary attribute that stores the historic variables from the Monte Carlo simulation


    Methods
    ----------
    draw_repair_time(dt)
        Decides and returns the repair time of the trafo based on a statistical distribution
    fail(dt)
        Sets the ICT node status to failed
    not_fail()
        Sets the ICT node to not failed
    update_fail_status(dt)
        Updates the fail status of the ICT node. Sets the fail status to failed if the ICT node is failed or the fail status to not failed if the ICT node is not failed
    print_status()
        Prints the status of the ICT node
    initialize_history()
        Initializes the history variables
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute at the ICT node
    add_random_instance(random_gen)
        Adds global random seed
    get_avg_fail_rate(curr_time)
        Returns the average failure rate of the ICT node
    reset_status(save_flag)
        Resets and sets the status of the class parameters
    get_monte_carlo_history(attribute)
        Returns a specified history variable from the Monte Carlo simulation
    """

    ## Visual attributes
    marker = "."
    size = 1.5**2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=2,
        markersize=size,
        linestyle="None",
    )

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        coordinate: list = [0, 0],
        fail_rate_per_year: float = 0.0,
        repair_time_dist: StatDist = StatDist(
            stat_dist_type=StatDistType.UNIFORM_FLOAT,
            parameters=UniformParameters(
                min_val=0.0,
                max_val=0.0,
            ),
        ),
    ):

        ## Informative attributes
        self.name = name
        self.coordinate = coordinate

        ## Topological attributes
        self.toline = None
        self.fromline = None
        self.toline_list = []
        self.fromline_list = []
        self.connected_lines = []
        self.parent_network = None

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_per_year  # failures per year
        self.repair_time_dist = repair_time_dist
        self.acc_outage_time = Time(0)
        self.avg_fail_rate = 0
        self.avg_outage_time = Time(0)
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.acc_interruptions = 0

        ## Status attribute
        self.failed = False
        self.remaining_outage_time = Time(0)

        ## History
        self.history = {}
        self.monte_carlo_history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ICTNode(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, ICTNode)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def draw_repair_time(self, dt: Time):
        """
        Decides and returns the repair time of the trafo based on a statistical distribution

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
        Sets the ICT node status to failed

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        self.failed = True
        self.remaining_outage_time = self.draw_repair_time(dt)

    def not_fail(self):
        """
        Sets the ICT node status to not failed

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.failed = False

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status of the ICT node. Sets the fail status to failed if the ICT node is failed or the fail status to not failed if the ICT node is not failed

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
        Prints the status of the ICT node

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        print(
            "name: {:3s}, failed={}".format(
                self.name,
                self.failed,
            )
        )

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
        self.history["avg_fail_rate"] = {}
        self.history["avg_outage_time"] = {}
        self.history["acc_outage_time"] = {}
        self.history["acc_interruptions"] = {}

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
        dt = curr_time - prev_time if prev_time is not None else curr_time
        self.acc_outage_time += dt if self.failed is True else Time(0)
        self.avg_outage_time = Time(
            self.acc_outage_time / curr_time, curr_time.unit
        )
        self.avg_fail_rate = self.get_avg_fail_rate(curr_time)

        if self.failed is True:
            self.num_consecutive_interruptions += 1
        else:
            if self.num_consecutive_interruptions >= 1:
                self.acc_interruptions += 1
            self.num_consecutive_interruptions = 0

        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["remaining_outage_time"][
                time
            ] = self.remaining_outage_time.get_unit_quantity(curr_time.unit)
            self.history["failed"][time] = self.failed
            self.history["avg_fail_rate"][
                time
            ] = self.avg_fail_rate  # Average failure rate (lamda_s)
            self.history["avg_outage_time"][
                time
            ] = self.avg_outage_time.get_unit_quantity(
                curr_time.unit
            )  # Average outage time (r_s)
            self.history["acc_outage_time"][
                time
            ] = self.acc_outage_time.get_unit_quantity(
                curr_time.unit
            )  # Accumulated outage time
            self.history["acc_interruptions"][
                time
            ] = self.acc_interruptions

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute at the ICT node

        Parameters
        ----------
        attribute : str
            ICT node attribute

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

    def get_avg_fail_rate(self, curr_time: Time):
        """
        Returns the average failure rate of the ICT node

        Parameters
        ----------
        None

        Returns
        ----------
        avg_fail_rate : float
            The average failure rate of the ICT node

        """
        fail_rate = self.fail_rate_per_year
        if self.parent_network is not None:
            for line in self.parent_network.get_lines():
                fail_rate += line.fail_rate_per_year
        avg_fail_rate = fail_rate / curr_time.get_years()
        return avg_fail_rate

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
        self.failed = False
        self.remaining_outage_time = Time(0)
        self.acc_outage_time = Time(0)
        self.num_consecutive_interruptions = 0
        self.acc_interruptions = 0
        if save_flag:
            self.initialize_history()

    def get_monte_carlo_history(self, attribute):
        """
        Returns a specified history variable from the Monte Carlo simulation

        Parameters
        ---------
        attribute : str
            ICT node attribute

        Returns
        --------
        monte_carlo_history[attribute] : str
            The specified history variable from the Monte Carlo simulation
        """
        return self.monte_carlo_history[attribute]

    def get_neighbor_nodes(self):
        """
        Returns the neighboring nodes of the node

        Parameters
        ---------
        None

        Returns
        --------
        neighbor_nodes : list
            List of neighboring nodes
        """
        neighbor_nodes = []
        for line in self.connected_lines:
            if line.connected is True:
                for node in [line.fnode, line.tnode]:
                    if node not in neighbor_nodes and node != self:
                        neighbor_nodes.append(node)

        return neighbor_nodes
