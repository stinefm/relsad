from relsad.network.components import Bus, DistributionController, Line
from relsad.utils import unique

from .PowerNetwork import PowerNetwork
from .PowerSystem import PowerSystem


class Distribution(PowerNetwork):

    """
    Class defining a distribution network type

    ...

    Attributes
    ----------
    name : str
        Name of the distribution network
    buses : list
        List containing the buses connected to the distribution network
    ev_parks : list
        List containing the EV parks in the distribution network
    batteries : list
        List containing the batteries in the distribution network
    productions : list
        List containing the generation units in the distribution network
    lines : list
        List containing the lines connected to the distribution network
    sensors : list
        List containing the sensors in the distribution network
    circuitbreaker : list
        List containing the circuit breakers in the distribution network
    disconnectors : list
        List containing the disconnectors in the distribution network
    intelligent_switches : list
        List containing the intelligent switches in the distribution network
    controller : DistributionController
        The controller for the distribution system
    comp_list : list
        List containing the components in the distribution network
    comp_dict : dict
        Dictionary containing the components in the distribution network
    parent_network : PowerNetwork
        The parent network of the distribution network
    power_system : PowerNetwork
        Connects the distribution network to a power system
    child_network_list : list
        List containing connected child networks to the distribution network
    failed_line : Bool
        Flag stating if the distribution network contains a failed line
    p_energy_shed : float
        Shedded active power load in the distribution network
    acc_p_energy_shed : float
        The accumulated shedded active power load in the distribution network
    q_energy_shed : float
        Shedded reactive power load in the distribution network
    acc_q_energy_shed : float
        The accumulated shedded reactive power load in the distribution network
    connected_line : Line
        Connects the distribution network to the transmission network, the line connecting the distribution network to the transmission network
    add_connected_line : Line
        Adds the connected line to the distribution network
    sections : Section
        The sections in the distribution system
    history : dict
        Dictionary containing the history variables of the network
    monte_carlo_history : dict
        Dictionary containing the history variables from the monte carlo simulation



    Methods
    ----------
    add_connected_line(connected_line)
        Sets the line connecting the distribution system to overlying network
    add_bus(bus)
        Adding a bus including elements on the bus (battery, generation unit, EV park) to the distribution network
    add_buses(buses)
        Adding buses to the distribution network
    add_line(line)
        Adding a line including elements on the line (sensor, circuit breaker, disconnector) to the distribution network
    add_lines(lines)
        Adding lines to the distribution network
    get_lines()
        Returns the lines in the distribution network
    reset_slack_bus()
        Resets the slack bus attribute of the buses in the distribution network
    add_child_network(network)
        Adds child network to the distribution network
    get_monte_carlo_history(attribute)
        Returns the specified history variable from the Monte Carlo simulation
    get_history(attribute)
        Returns the specified history variable
    get_system_load()
        Returns the load in the distribution network at the current time in MW and MVar
    reset_energy_shed_variables()
        Resets the energy.shed variables
    """

    ## Visual attributes
    color = "steelblue"

    ## Counter
    counter = 0

    def __init__(self, parent_network: PowerNetwork, connected_line: Line):
        Distribution.counter += 1
        self.name = "dist_network{:d}".format(Distribution.counter)

        # Components
        self.buses = list()
        self.ev_parks = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()
        self.sensors = list()
        self.circuitbreakers = list()
        self.disconnectors = list()
        self.intelligent_switches = list()
        self.controller = DistributionController(
            name=self.name + "_controller",
            power_network=self,
        )
        self.comp_list = list()
        self.comp_dict = dict()

        # PowerNetwork connections
        self.parent_network = parent_network
        parent_network.add_child_network(self)
        if isinstance(parent_network, PowerSystem):
            self.power_system = parent_network
        else:
            self.power_system = parent_network.parent_network
        self.power_system.controller.add_distribution_controller(
            self.controller
        )
        self.child_network_list = list()
        self.power_system.comp_dict[self.controller.name] = self.controller
        self.power_system.comp_list.append(self.controller)

        self.failed_line = False
        # Load shedding
        self.p_energy_shed = 0
        self.acc_p_energy_shed = 0
        self.q_energy_shed = 0
        self.acc_q_energy_shed = 0

        self.connected_line = None
        if connected_line is not None:
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
        """
        Sets the line connecting the distribution system to overlying network

        Parameters
        ----------
        connected_line : Line
            The line connecting the distribution system to overlaying network

        Returns
        ----------
        None

        """
        # Sets the connected line for the distribution system
        self.connected_line = connected_line

        # Add the components attached to the line
        # to the distribution system:

        # CircuitBreaker
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

        # Line
        self.add_line(connected_line)

    def add_bus(self, bus: Bus):
        """
        Adding a bus including elements on the bus (battery, generation unit, EV park) to the distribution network

        Parameters
        ----------
        bus : Bus
            A Bus element

        Returns
        ----------
        None

        """
        # Add bus to distribution network
        self.comp_dict[bus.name] = bus
        bus.handle.color = self.color
        bus.color = self.color
        bus.parent_network = self
        self.buses.append(bus)
        self.buses = unique(self.buses)

        # Add components attached to bus to distribution network:

        # EV-Park
        if bus.ev_park is not None:
            self.comp_dict[bus.ev_park.name] = bus.ev_park
            self.comp_list.append(bus.ev_park)
            self.ev_parks.append(bus.ev_park)
            self.ev_parks = unique(self.ev_parks)

        # Battery
        if bus.battery is not None:
            self.comp_dict[bus.battery.name] = bus.battery
            self.comp_list.append(bus.battery)
            self.batteries.append(bus.battery)
            self.batteries = unique(self.batteries)

        # Production
        if bus.prod is not None:
            self.comp_dict[bus.prod.name] = bus.prod
            self.comp_list.append(bus.prod)
            self.productions.append(bus.prod)
            self.productions = unique(self.productions)

        # Add bus to the power system
        self.power_system.add_bus(bus)

    def add_buses(self, buses: list):
        """
        Adding buses to the distribution network bus list

        Parameters
        ----------
        buses : list
            A list of Bus elements in the distribution network

        Returns
        ----------
        None

        """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding a line and the components connected to the line to the distribution network

        Parameters
        ----------
        line : Line
            A Line element

        Returns
        ----------
        None

        """

        # Add line to distribution network
        line.handle.color = self.color
        line.color = self.color
        self.comp_dict[line.name] = line
        self.lines.append(line)
        self.lines = unique(self.lines)

        # Add components attached to line to distribution network:

        # Sensor
        if line.sensor:
            self.comp_dict[line.sensor.name] = line.sensor
            self.comp_list.append(line.sensor)
            self.sensors.append(line.sensor)
            self.sensors = unique(self.sensors)
            self.controller.sensors.append(line.sensor)
            self.controller.sensors = unique(self.controller.sensors)

        # Disconnector
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
            self.comp_list.append(discon)
            self.disconnectors.append(discon)
            self.disconnectors = unique(self.disconnectors)

            # Intelligent switch
            if discon.intelligent_switch:
                self.comp_dict[
                    discon.intelligent_switch.name
                ] = discon.intelligent_switch
                self.comp_list.append(discon.intelligent_switch)
                self.intelligent_switches.append(discon.intelligent_switch)
                self.intelligent_switches = unique(self.intelligent_switches)

        # Set distribution network as parent network
        line.add_parent_network(self)

        # Add line to power system
        self.power_system.add_line(line)

    def add_lines(self, lines: list):
        """
        Adding lines to distribution network line list

        Parameters
        ----------
        lines : list
            A list of Line elements in the distribution network

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
            List of Line elements

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
        network : PowerNetwork
            The child network of the distribution network

        Returns
        ----------
        None

        """
        self.child_network_list.append(network)
        self.parent_network.add_child_network(network)

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable from the Monte Carlo simulation

        Parameters
        ----------
        attribute : str
            Distribution network attribute

        Returns
        ----------
        monte_carlo_history[attribute] : dict
            Returns the history variables of an attribute from the Monte Carlo simulation

        """
        return self.monte_carlo_history[attribute]

    def get_history(self, attribute):
        """
        Returns the specified history variable

        Parameters
        ----------
        attribute : str
            Distribution network attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def get_system_load(self):
        """
        Returns the system load in the distribution network at the current time in MW and MVar

        Parameters
        ----------
        None

        Returns
        ----------
        pload : float
            The active power load in the distribution network
        qload : float
            The reactive power load in the distribution network

        """
        pload, qload = 0, 0
        for bus in self.buses:
            p, q = bus.get_load()
            pload += p
            qload += q
        return pload, qload

    def reset_energy_shed_variables(self):
        """
        Resets the energy.shed variables

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.p_energy_shed = 0
        self.acc_p_energy_shed = 0
        self.q_energy_shed = 0
        self.acc_q_energy_shed = 0
