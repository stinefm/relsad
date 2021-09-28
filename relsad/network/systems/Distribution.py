from relsad.network.components import Bus, Line, DistributionController
from .Network import Network
from .Transmission import Transmission
from relsad.utils import unique


class Distribution(Network):

    """
    Class defining a distribution network type

    ...

    Attributes
    ----------
    name : str
        Name of the distribution network
    buses : Bus
        List with the buses connected to the distribution network
    lines : Lines
        List with the lines connected to the distribution network
    comp_dict : dict
        Dictionary containing the components connected to the distribution network
    parent_network : Network
        The parent network of the distribution network
    power_system : Network
        Connects the distribution network to a power system ?
    child_network_list : list
        List containing connected child networks to the distribution network
    failed_line : Bool
        ?
    connected_line : Line
        Connects the distribution network to the transmission network, chooses line connecting the distribution network to the transmission network


    Methods
    ----------
    add_bus(bus)
        Adding bus to distribution network
    add_buses(buses)
        Adding buses to distribution network
    add_line(line)
        Adding line to distribution network
    add_lines(lines)
        Adding lines to distribution network
    get_lines()
        Returns the lines in the distribution network
    reset_slack_bus()
        Resets the slack bus attribute of the buses in the distribution network
    add_child_network(network)
        Adds child network to the distribution network



    """

    ## Visual attributes
    color = "steelblue"

    ## Counter
    counter = 0

    def __init__(
        self, transmission_network: Transmission, connected_line: Line
    ):
        """Initializing distributed network type content
        Content:
            buses(set): List of buses
            lines(set): List of lines
            comp_dict(dict): Dictionary of components
            connected_line(Line): Line connected to distrubution network
        """
        Distribution.counter += 1
        self.name = "dist_network{:d}".format(Distribution.counter)

        # Components
        self.buses = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()
        self.sensors = list()
        self.circuitbreakers = list()
        self.disconnectors = list()
        self.intelligent_switches = list()
        self.controller = DistributionController(
            name=self.name + "_controller",
            network=self,
        )
        self.comp_list = list()
        self.comp_dict = dict()

        # Network connections
        self.parent_network = transmission_network
        transmission_network.add_child_network(self)
        self.power_system = transmission_network.parent_network
        self.power_system.controller.add_distribution_controller(
            self.controller
        )
        self.child_network_list = list()
        self.power_system.comp_dict[self.controller.name] = self.controller
        self.power_system.comp_list.append(self.controller)

        self.failed_line = False
        # Load shedding
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0

        self.connected_line = None
        self.add_connected_line(connected_line)

        # Sectioning
        self.sections = None
        ## History
        self.history: dict = {}
        self.monte_carlo_history: dict = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Distribution(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_connected_line(self, connected_line):
        self.connected_line = connected_line
        c_b = connected_line.circuitbreaker
        if self.connected_line.circuitbreaker is None:
            raise Exception(
                "{} connects the distribution network to the "
                "transmission network, it must contain a circuitbreaker".format(
                    connected_line
                )
            )
        self.comp_dict[c_b.name] = c_b
        self.comp_list.append(c_b)
        for discon in c_b.disconnectors:
            self.comp_dict[discon.name] = discon
            if discon.intelligent_switch:
                self.comp_dict[
                    discon.intelligent_switch.name
                ] = discon.intelligent_switch
                self.comp_list.append(discon.intelligent_switch)
                self.intelligent_switches.append(discon.intelligent_switch)
                self.intelligent_switches = unique(self.intelligent_switches)
        self.add_line(connected_line)

    def add_bus(self, bus: Bus):
        """
        Adding bus to distribution network

        Parameters
        ----------
        bus : Bus
            A Bus element

        Returns
        ----------
        None

        """
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
        self.power_system.add_bus(bus)

    def add_buses(self, buses: set):
        """
        Adding buses to distribution network

        Parameters
        ----------
        buses : list
            A list of buses connected to the distribution network

        Returns
        ----------
        None

        """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding line to distribution network

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
        self.comp_dict[line.name] = line
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
        self.lines.append(line)
        self.lines = unique(self.lines)
        if line.sensor:
            self.comp_dict[line.sensor.name] = line.sensor
            self.comp_list.append(line.sensor)
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
                self.comp_dict[
                    discon.intelligent_switch.name
                ] = discon.intelligent_switch
                self.comp_list.append(discon.intelligent_switch)
                self.intelligent_switches.append(discon.intelligent_switch)
                self.intelligent_switches = unique(self.intelligent_switches)
        line.add_parent_network(self)
        self.power_system.add_line(line)

    def add_lines(self, lines: set):
        """
        Adding lines to distribution network

        Parameters
        ----------
        lines : list
            A list of lines connected to the distribution network

        Returns
        ----------
        None

        """
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the distribution network

        Parameters
        ----------
        None

        Returns
        ----------
        lines : list
            Returns a list with the lines in the distribution network

        """
        return self.lines

    def reset_slack_bus(self):
        """
        Resets the slack bus attribute of the buses in the distribution network

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        for bus in self.buses:
            bus.is_slack = False

    def add_child_network(self, network):
        """
        Adds child network to the distribution network

        Parameters
        ----------
        network : Network
            The child network of the distribution network

        Returns
        ----------
        None

        """
        self.child_network_list.append(network)
        self.parent_network.add_child_network(network)

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
