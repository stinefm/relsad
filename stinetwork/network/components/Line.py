import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Bus import Bus
from stinetwork.utils import random_choice


class Line(Component):
    r"""
    A class used to represent an electrical Line

    ...

    Attributes
    ----------
    name : str
        Name of the line
    is_backup : bool
        Decides if the line is a backup line
    fbus : Bus
        Sending bus
    tbus : Bus
        Receiving bus
    disconnectors : list
        List of disconnectors connected to the line
    circuitbreaker : Circuitbreaker
        Circuit breaker connected to the line
    parent_network : Network
        The parent network of the line
    r : float
        Resistance \[Ohm\]
    x : float
        Reactance \[\]
    length : float
        Length of line \[km\]
    capacity : float
        The capacity of the line \[MW\]
    ploss : float
        The active power loss over the line \[MW\]
    qloss : float
        The reactive power loss over the line \[MW\]
    fail_rate_per_year : float
        Failure rate per year \[fault/year/km\]
    fail_rate_per_hour : float
        Failure rate per hour \[fault/hour/km\]
    outage_time : float
        Outage time \[hours/fault\]
    connected : str
        Line state
    failed : bool
        Failure status of the line
    remaining_outage_time : float
        The remaining outage time of the line
    history : dict
        Dictonary attribute that stores the historic variables


    Methods
    -------
    set_backup()
        Sets the backup lines and opens the disconnectors connected to the backup line
    disconnect()
        Disconnects a line and removes the line
    connect()
        Connects a line and append the line
    fail()
        Sets the fail status of the line to True and opens the connected disconnectors and the connected circuit breaker
    not_fail()
        Sets the fail status of the line to False and closes the connected disconnectors and connected circuit breaker
    change_direciton()
        Changes the direction of the line
    update_fail_status()
        Updates the fail status of the line
    get_line_load()
        Gets the power flow over the line
        Returns the flow over the line
    get_line_loading()
        Returns the line loading of the line in percentage
    print_status()
        Prints the line status
    get_disconnetors()
        Returns the connected disconnectors
    add_parent_network(network)
        Adds the parent network to the line
    update_history(curr_time)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_seed(random_gen)
        Adds global random seed
    reset_status()
        Resets and sets the status of the class parameters
    """
    lineCount = 0

    ## Visual attributes
    linestyle = "-"
    handle = mlines.Line2D([], [], linestyle=linestyle)

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        fbus: Bus,
        tbus: Bus,
        r: float,  # Ohm
        x: float,  # Ohm
        s_ref: float = 1,  # MVA
        v_ref: float = 12.66,  # kV
        rho: float = 1.72e-8,  # resistivity [Ohm*m]
        area: float = 64.52e-6,  # cross-sectional area [m**2]
        fail_rate_density_per_year: float = 0.2,
        outage_time: float = 4,
        capacity: float = 100,  # MW
        connected=True,
    ):
        ## Informative attributes
        self.name = name

        ## Backup
        self.is_backup = False

        ## Topological attributes
        self.fbus = fbus
        self.tbus = tbus
        fbus.connected_lines.append(self)
        tbus.connected_lines.append(self)
        tbus.toline = self
        tbus.toline_list.append(self)
        fbus.fromline = self
        fbus.fromline_list.append(self)
        fbus.nextbus.append(self.tbus)
        self.disconnectors = list()
        self.circuitbreaker = None
        self.parent_network = None
        self.section = None
        Line.lineCount += 1

        ##  Power flow attributes
        self.s_ref = s_ref
        self.v_ref = v_ref
        self.r_ref = v_ref ** 2 / s_ref
        self.r = r
        self.x = x
        self.r_pu = r / self.r_ref
        self.x_pu = x / self.r_ref
        self.area = area
        self.rho = rho
        self.length = r * area / rho * 1e-3  # km
        self.capacity = capacity  # MW
        self.ploss = 0.0
        self.qloss = 0.0

        ## Reliabilility attributes
        self.fail_rate_per_year = (
            fail_rate_density_per_year * self.length
        )  # failures per year
        self.fail_rate_per_hour = self.fail_rate_per_year / (365 * 24)
        self.outage_time = outage_time  # hours

        ## Status attribute
        self.connected = connected
        self.failed = False
        self.remaining_outage_time = 0

        ## Communication
        self.sensor = None

        ## History
        self.history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Line(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Line)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def set_backup(self):
        """
        Sets the backup lines and opens the disconnectors connected to the backup line

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.is_backup = True
        for discon in self.disconnectors:
            discon.open()

    def disconnect(self):
        """
        Disconnects a line and removes the line

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.connected = False
        self.linestyle = "--"
        self.fbus.fromline_list.remove(self)
        if self.fbus.fromline == self:
            if len(self.fbus.fromline_list) > 0:
                self.fbus.fromline = next(iter(self.fbus.fromline_list))
            else:
                self.fbus.fromline = None
        self.tbus.toline_list.remove(self)
        if self.tbus.toline == self:
            if len(self.tbus.toline_list) > 0:
                self.tbus.toline = next(iter(self.tbus.toline_list))
            else:
                self.tbus.toline = None
        self.fbus.nextbus.remove(self.tbus)

    def connect(self):
        """
        Connects a line and append the line

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.connected = True
        self.linestyle = "-"
        self.tbus.toline = self
        self.tbus.toline_list.append(self)
        self.fbus.fromline = self
        self.fbus.fromline_list.append(self)
        self.fbus.nextbus.append(self.tbus)

    def fail(self):
        """
        Sets the fail status of the line to False and opens the connected disconnectors and the connected circuit breaker

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.failed = True
        self.parent_network.failed_line = True
        self.remaining_outage_time = self.outage_time
        if self.connected:
            # Relay
            self.parent_network.connected_line.circuitbreaker.open()
            if self.parent_network.child_network_list is not None:
                for child_network in self.parent_network.child_network_list:
                    child_network.connected_line.circuitbreaker.open()

    def not_fail(self):
        """
        Sets the fail status of the line to False and closes the connected disconnectors and connected circuit breaker

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
        self.fbus.fromline_list.remove(self)
        self.tbus.fromline_list.append(self)
        self.tbus.toline_list.remove(self)
        self.fbus.toline_list.append(self)
        if self.fbus.fromline == self:
            self.fbus.fromline = (
                next(iter(self.fbus.fromline_list))
                if len(self.fbus.fromline_list) > 0
                else None
            )
        if self.tbus.toline == self:
            self.tbus.toline = (
                next(iter(self.tbus.toline_list))
                if len(self.tbus.toline_list) > 0
                else None
            )
        self.fbus.toline = self
        self.tbus.fromline = self
        self.fbus.nextbus.remove(self.tbus)
        self.tbus.nextbus.append(self.fbus)
        i_broken = self.tbus.num
        self.tbus.num = self.fbus.num
        self.fbus.num = i_broken
        bus = self.fbus
        self.fbus = self.tbus
        self.tbus = bus

    def update_fail_status(self):
        """
        Updates the fail status of the line

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.is_backup:
            for discon in self.disconnectors:
                if not discon.is_open:
                    discon.open()
        if self.failed:
            self.remaining_outage_time -= 1
            if self.remaining_outage_time == 0:
                self.not_fail()
        else:
            p_fail = self.fail_rate_per_hour
            if random_choice(self.ps_random, p_fail):
                self.fail()
            else:
                self.not_fail()

    def get_line_load(self):
        """
        Returns the flow over the line in PU

        Parameters
        ----------
        None

        Returns
        ----------
        p_from : float
            The active power sent from the line
        q_from : float
            The reactive power sent from the line
        p_to : float
            The active power sent to the line
        q_to : float
            The reactive power sent to the line

        """

        def uij(gij, bij, tetai, tetaj):
            return gij * np.sin(tetai - tetaj) - bij * np.cos(tetai - tetaj)

        def tij(gij, bij, tetai, tetaj):
            return gij * np.cos(tetai - tetaj) + bij * np.sin(tetai - tetaj)

        def bij(R, X):
            return (1.0 / complex(R, X)).imag

        def gij(R, X):
            return (1.0 / complex(R, X)).real

        if self.connected:
            fbus = self.fbus
            tbus = self.tbus
            bsh = 0.0  # No shunts included so far
            teta1 = fbus.voang
            teta2 = tbus.voang
            v1 = fbus.vomag
            v2 = tbus.vomag
            b = bij(self.r_pu, self.x_pu)
            g = gij(self.r_pu, self.x_pu)

            p_from = g * v1 * v1 - v1 * v2 * tij(g, b, teta1, teta2)
            p_to = g * v2 * v2 - v1 * v2 * tij(g, b, teta2, teta1)
            q_from = -(b + bsh) * v1 * v1 - v1 * v2 * uij(g, b, teta1, teta2)
            q_to = -(b + bsh) * v2 * v2 - v1 * v2 * uij(g, b, teta2, teta1)

            return p_from, q_from, p_to, q_to
        else:
            return 0, 0, 0, 0

    def get_line_loading(self):
        """
        Returns the line loading of the line in percentage

        Parameters
        ----------
        None

        Returns
        ----------
        line_loading : float
            The line loading of the line

        """

        p_from = self.get_line_load()[0]
        line_loading = abs(p_from) / (self.capacity / self.s_ref) * 100
        return line_loading

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

    def get_disconnectors(self):
        """
        Returns the connected disconnectors

        Parameters
        ----------
        None

        Returns
        ----------
        disconnectors : Disconnector
            Disconnector connected to the line

        """
        return self.disconnectors

    def add_parent_network(self, network):
        """
        Adds the parent network to the line

        Parameters
        ----------
        network : Network
            The parent network of the line

        Returns
        ----------
        None

        """

        self.parent_network = network

    def initialize_history(self):
        self.history["p_from"] = {}
        self.history["q_from"] = {}
        self.history["p_to"] = {}
        self.history["q_to"] = {}
        self.history["remaining_outage_time"] = {}
        self.history["failed"] = {}
        self.history["line_loading"] = {}

    def update_history(self, prev_time, curr_time, save_flag: bool):
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
            p_from, q_from, p_to, q_to = self.get_line_load()
            self.history["p_from"][curr_time] = p_from * self.s_ref
            self.history["q_from"][curr_time] = q_from * self.s_ref
            self.history["p_to"][curr_time] = p_to * self.s_ref
            self.history["q_to"][curr_time] = q_to * self.s_ref
            self.history["remaining_outage_time"][
                curr_time
            ] = self.remaining_outage_time
            self.history["failed"][curr_time] = self.failed
            self.history["line_loading"][curr_time] = self.get_line_loading()

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
        self.remaining_outage_time = 0

        self.not_fail()
        if save_flag:
            self.initialize_history()

    def reset_load_flow_data(self):
        """
        Resets the variables used in the load flow analysis
        """
        self.ploss = 0
        self.qloss = 0


if __name__ == "__main__":
    pass
