from stinetwork.network.components import (
    Bus,
    Line,
    MicrogridController,
    MicrogridMode,
)
from .Network import Network
from .Distribution import Distribution
from stinetwork.utils import unique


class Microgrid(Network):
    """
    Class defining a microgrid network type

    ...

    Attributes
    ----------
    name : str
        Name of the microgrid
    mode : str
        Which mode the microgrid follows
    buses : Bus
        List with the buses connected to the microgrid
    lines : Lines
        List with the lines connected to the microgrid
    comp_dict : dict
        Dictionary containing the components connected to the microgrid
    distribution_network : Network
        The distribution network the microgrid is connected to
    child_network_list : list
        List containing connected child networks to the microgrid ?
    failed_line : Bool
        Boolean value stating whether or not the network includes a failed line
    connected_line : Line
        Line that connects the microgrid to the distribution network
    circuitbreaker : Circuitbreaker
        The circuitbreaker connected to the line

    Methods
    ----------
    add_bus(bus)
        Adding bus to microgrid
    add_buses(buses)
        Adding buses to microgrid
    add_line(line)
        Adding line to microgrid
    add_lines(lines)
        Adding lines to microgrid
    get_lines()
        Returns the lines in the microgrid
    connect(self)
        Connects microgrid to parent distribution network by closing the disconnectors on the microgrid lines
    disconnect()
         Disconnects microgrid to parent distribution network by opening the disconnectors on the microgrid lines
    reset_slack_bus()
        Resets the slack bus attribute of the buses in the microgrid
    get_max_load()
        Get the max load of the microgrid load and returns the max load

    """

    ## Visual attributes
    color = "orange"

    ## Counter
    counter = 0

    def __init__(
        self,
        distribution_network: Distribution,
        connected_line: Line,
        mode: MicrogridMode = MicrogridMode.SURVIVAL,
    ):
        """Initializing microgrid network type content
        Content:
            mode(MicrogridMode): Microgrid mode, 1) survival, 2) full support, 3) limited support

            buses(list): List of buses
            lines(list): List of lines
            comp_dict(dict): Dictionary of components
            connected_line(Line): Line connected to distrubution network
        """
        Microgrid.counter += 1
        self.name = "microgrid{:d}".format(Microgrid.counter)
        self.mode = mode

        # Components
        self.buses = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()
        self.sensors = list()
        self.circuitbreakers = list()
        self.disconnectors = list()
        self.intelligent_switches = list()
        self.controller = MicrogridController(
            name=self.name + "_controller",
            network=self,
        )
        self.comp_list = list()
        self.comp_dict = dict()

        # Network connections
        self.distribution_network = distribution_network
        self.distribution_network.add_child_network(self)
        self.distribution_network.power_system.controller.add_microgrid_controller(
            self.controller
        )
        self.child_network_list = None
        self.distribution_network.power_system.comp_dict[
            self.controller.name
        ] = self.controller
        self.distribution_network.power_system.comp_list.append(
            self.controller
        )

        self.failed_line = False

        self.connected_line = connected_line
        self.circuitbreaker = connected_line.circuitbreaker
        self.circuitbreaker.mode = mode
        if self.circuitbreaker is None:
            raise Exception(
                "{} connects the microgrid to the "
                "distribution network, it must contain a circuitbreaker".format(
                    connected_line
                )
            )
        self.comp_dict[self.circuitbreaker.name] = self.circuitbreaker
        for discon in self.circuitbreaker.disconnectors:
            self.comp_dict[discon.name] = discon
        self.add_line(connected_line)
        # Load shedding
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0
        # Sectioning
        self.sections = None
        ## History
        self.history: dict = {}
        self.monte_carlo_history: dict = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Microgrid(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus: Bus):
        """
        Adding bus to microgrid

        Parameters
        ----------
        bus : Bus
            A Bus element

        Returns
        ----------
        None

        """
        if bus.get_battery() is not None:
            bus.get_battery().set_mode(self.mode)
        self.comp_dict[bus.name] = bus
        bus.handle.color = self.color
        bus.color = self.color
        bus.parent_network = self
        self.buses.append(bus)
        self.buses = unique(self.buses)
        if bus.battery is not None:
            self.comp_dict[bus.battery.name] = bus.battery
            self.comp_list.append(bus.battery)
            self.batteries.append(bus.battery)
            self.batteries = unique(self.batteries)
        if bus.prod is not None:
            self.comp_dict[bus.prod.name] = bus.prod
            self.comp_list.append(bus.prod)
            self.productions.append(bus.prod)
            self.productions = unique(self.productions)
        self.distribution_network.power_system.add_bus(bus)

    def add_buses(self, buses: list):
        """
        Adding buses to microgrid


        Parameters
        ----------
        buses : list
            A list of buses connected to the microgrid

        Returns
        ----------
        None

        """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding line to microgrid


        Parameters
        ----------
        line : Line
            A Line element

        Returns
        ----------
        None

        """
        line.handle.color = self.color
        line.color = self.color
        self.lines.append(line)
        self.lines = unique(self.lines)
        if line.sensor:
            self.sensors.append(line.sensor)
            self.sensors = unique(self.sensors)
            self.controller.sensors.append(line.sensor)
            self.controller.sensors = unique(self.controller.sensors)
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
            self.comp_list.append(discon)
            self.disconnectors.append(discon)
            self.disconnectors = unique(self.disconnectors)
            if discon.intelligent_switch:
                self.intelligent_switches.append(discon.intelligent_switch)
                self.intelligent_switches = unique(self.intelligent_switches)
        line.add_parent_network(self)
        self.distribution_network.power_system.add_line(line)

    def add_lines(self, lines: list):
        """
        Adding lines to microgrid

        Parameters
        ----------
        lines : list
            A list of lines connected to the microgrid

        Returns
        ----------
        None

        """
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the microgrid

        Parameters
        ----------
        None

        Returns
        ----------
        lines : list
            Returns a list with the lines in the microgrid

        """
        return self.lines

    def connect(self):
        """
        Connects microgrid to parent distribution network by closing the disconnectors on the microgrid lines


        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for discon in self.connected_line.get_disconnectors():
            if discon.is_open:
                discon.close()

    def disconnect(self):
        """
        Disconnects microgrid to parent distribution network by opening the disconnectors on the microgrid lines

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for discon in self.connected_line.get_disconnectors():
            if not discon.is_open:
                discon.open()

    def reset_slack_bus(self):
        """
        Resets the slack bus attribute of the buses in the microgrid

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.is_slack = False

    def get_max_load(self):
        """
        Get the maximum load of the microgrid for the entire loading history

        Parameters
        ----------
        None

        Returns
        ----------
        p_load_max : float
            The maximum active load of the microgrid for the entire loading history

        q_load_max : float
            The maximum reactive load of the microgrid for the entire loading history

        """
        p_load_max, q_load_max = 0, 0
        for bus in self.buses:
            if bus.load_dict != dict():
                d_bus = bus  # Dummy bus used to find number of increments
                n_increments = len(
                    d_bus.load_dict[list(d_bus.load_dict.keys())[0]][
                        "pload"
                    ].flatten()
                )  # Number of increments
                break
        for increment in range(n_increments):
            p_load, q_load = 0, 0
            for bus in self.buses:
                for load_type in bus.load_dict:
                    p_load += (
                        bus.load_dict[load_type]["pload"].flatten()[increment]
                        * bus.n_customers
                    )
                    q_load += (
                        bus.load_dict[load_type]["qload"].flatten()[increment]
                        * bus.n_customers
                    )
            p_load_max = max(p_load_max, p_load)
            q_load_max = max(q_load_max, q_load)
        return p_load_max, q_load_max

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable
        """
        return self.monte_carlo_history[attribute]

    def get_history(self, attribute):
        """
        Returns the specified history variable
        """
        return self.history[attribute]

    def get_system_load(self):
        """
        Returns the system load at curr_time in MW/MVar
        """
        pload, qload = 0, 0
        for bus in self.buses:
            p, q = bus.get_load()
            pload += p
            qload += q
        return pload, qload

    def reset_load_shed_variables(self):
        """
        Resets the load shed variables
        """
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0
