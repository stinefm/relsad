import matplotlib.lines as mlines
import numpy as np

from relsad.StatDist import StatDist, StatDistType, UniformParameters
from relsad.Time import Time, TimeUnit
from relsad.utils import convert_yearly_fail_rate, random_choice

from .Bus import Bus
from .Component import Component


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
    circuitbreaker : CircuitBreaker
        Circuit breaker connected to the line
    parent_network : PowerNetwork
        The parent network of the line
    section : Section
        The section the line belongs to
    s_ref : float
        Reference apperet power [MVA]
    v_ref : float
        Reference voltage [kV]
    r_ref : float
        Reference resistance [Ohm]
    r : float
        Resistance [Ohm]
    x : float
        Reactance [Ohm]
    r_pu : float
        The pu value of the resistance
    x_pu : float
        The pu value of the reactance
    area : float
        The cross-sectional area [m^2]
    rho : float
        The resistivity of the line [Ohm*m]
    length : float
        Length of line [km]
    capacity : float
        The capacity of the line [MW]
    ploss : float
        The active power loss over the line [MW]
    qloss : float
        The reactive power loss over the line [MVar]
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
    sensor : Sensor
        The sensor(s) connected to the line
    history : dict
        Dictonary attribute that stores the historic variables


    Methods
    -------
    set_backup()
        Sets the backup lines and opens the disconnectors connected to the backup line
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
    get_line_load()
        Returns the flow over the line in PU values
    get_line_loading()
        Returns the loading of the line in percentage
    print_status()
        Prints the line status
    get_disconnetors()
        Returns the connected disconnectors
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
    reset_load_flow_data()
        Resets the variables used in the load flow analysis
    get_switches()
        Returns the switches on the line
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
        repair_time_dist: StatDist = StatDist(
            stat_dist_type=StatDistType.UNIFORM_FLOAT,
            parameters=UniformParameters(
                min_val=0.0,
                max_val=0.0,
            ),
        ),
        s_ref: float = 1,  # MVA
        v_ref: float = 12.66,  # kV
        rho: float = 1.72e-8,  # resistivity [Ohm*m]
        area: float = 64.52e-6,  # cross-sectional area [m**2]
        fail_rate_density_per_year: float = 0.0,  # fails/(km*year)
        capacity: float = 100,  # MW
        connected=True,
    ):

        # Verify input
        if fbus is None:
            raise Exception("Line must have a origin bus")
        if tbus is None:
            raise Exception("Line must have a target bus")
        if r < 0:
            raise Exception("r must be positive")
        if x < 0:
            raise Exception("x must be positive")
        if repair_time_dist is None:
            raise Exception("The line must have a repair time distribution")
        if s_ref < 0:
            raise Exception("s_ref must be positive")
        if v_ref < 0:
            raise Exception("v_ref must be positive")
        if rho < 0:
            raise Exception("The resistivity must be positive")
        if area < 0:
            raise Exception("The line section area must be positive")
        if fail_rate_density_per_year < 0:
            raise Exception(
                "The failure rate density per year must be positive"
            )
        if capacity < 0:
            raise Exception("The line capacity must be positive")

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
        self.r_ref = v_ref**2 / s_ref
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
        self.repair_time_dist = repair_time_dist

        ## Status attribute
        self.connected = connected
        self.failed = False
        self.remaining_outage_time = Time(0)

        ## Communication

        self.sensor = None

        ## History
        self.history = {}
        self.initialize_history()

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
            self.tbus.toline = self
            self.tbus.toline_list.append(self)
            self.fbus.fromline = self
            self.fbus.fromline_list.append(self)
            self.fbus.nextbus.append(self.tbus)

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
        Sets the fail status of the line to False and opens the connected disconnectors and the connected circuit breaker

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
        if self.connected:
            # Relay

            # Disconnects parent network from its parent network
            self.parent_network.connected_line.circuitbreaker.open()

            # All child networks are disconnected from the parent network
            if hasattr(self.parent_network, "child_network_list"):
                if self.parent_network.child_network_list is not None:
                    for (
                        child_network
                    ) in self.parent_network.child_network_list:
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
        bus = self.fbus
        self.fbus = self.tbus
        self.tbus = bus

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
        if self.is_backup:
            for discon in self.disconnectors:
                if not discon.is_open:
                    discon.open()
        if self.failed:
            self.remaining_outage_time -= dt
            if self.remaining_outage_time <= Time(0):
                self.not_fail()
                self.parent_network.controller.check_components = True
                self.remaining_outage_time = Time(0)
        else:
            p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
            if random_choice(self.ps_random, p_fail):
                self.fail(dt)
            else:
                self.not_fail()

    def get_line_load(self):
        """
        Returns the flow over the line in PU values

        Parameters
        ----------
        None

        Returns
        ----------
        p_from : float
            The active power sent from the line [MW]
        q_from : float
            The reactive power sent from the line [MVar]
        p_to : float
            The active power sent to the line [MW]
        q_to : float
            The reactive power sent to the line [MVar]

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
        Returns the loading of the line in percentage

        Parameters
        ----------
        None

        Returns
        ----------
        line_loading : float
            The line loading

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
        self.history["p_from"] = {}
        self.history["q_from"] = {}
        self.history["p_to"] = {}
        self.history["q_to"] = {}
        self.history["remaining_outage_time"] = {}
        self.history["failed"] = {}
        self.history["line_loading"] = {}

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
            p_from, q_from, p_to, q_to = self.get_line_load()
            self.history["p_from"][time] = p_from * self.s_ref
            self.history["q_from"][time] = q_from * self.s_ref
            self.history["p_to"][time] = p_to * self.s_ref
            self.history["q_to"][time] = q_to * self.s_ref
            self.history["remaining_outage_time"][
                time
            ] = self.remaining_outage_time.get_unit_quantity(curr_time.unit)
            self.history["failed"][time] = self.failed
            self.history["line_loading"][time] = self.get_line_loading()

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

    def reset_load_flow_data(self):
        """
        Resets the variables used in the load flow analysis

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.ploss = 0
        self.qloss = 0

    def get_switches(self):
        """
        Returns the switches on the line

        Parameters
        ----------
        None

        Returns
        ----------
        switches
            The switches on the line

        """
        switches = (
            self.disconnectors + [self.circuitbreaker]
            if self.circuitbreaker is not None
            else self.disconnectors
        )
        return switches


if __name__ == "__main__":
    pass
