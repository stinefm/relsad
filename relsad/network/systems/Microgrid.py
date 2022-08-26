from relsad.network.components import (
    Bus,
    Line,
    MicrogridController,
    MicrogridMode,
)
from relsad.utils import unique

from .Distribution import Distribution
from .PowerNetwork import PowerNetwork


class Microgrid(PowerNetwork):
    """
    Class defining a microgrid network type

    ...

    Attributes
    ----------
    name : str
        Name of the microgrid
    mode : str
        Which mode the microgrid follows
    buses : list
        List with the buses in the microgrid
    ev_parks : list
        List containing the EV parks in the microgrid
    batteries : list
        List containing the batteries in the microgrid
    productions : list
        List containing the generation units in the microgrid
    lines : list
        List with the lines in the microgrid
    sensors : list
        List containing the sensors in the microgrid
    circuitbreaker : list
        List containing the circuit breakers in the microgrid
    disconnectors : list
        List containing the disconnectors in the microgrid
    intelligent_switches : list
        List containing the intelligent switches in the microgrid
    controller : MicrogridController
        The controller for the microgrid
    comp_list : list
        List containing the components in the microgrid
    comp_dict : dict
        Dictionary containing the components in the microgrid
    distribution_network : PowerNetwork
        The distribution network the microgrid is connected to
    failed_line : Bool
        Boolean value stating whether or not the network includes a failed line
    connected_line : Line
        Line that connects the microgrid to the distribution network
    circuitbreaker : CircuitBreaker
        The circuitbreaker connected to the line
    p_energy_shed : float
        Shedded active power in the microgrid
    acc_p_energy_shed : float
        The accumulated shedded active power in the microgrid
    q_energy_shed : float
        Shedded reactive power in the microgrid
    acc_q_energy_shed : float
        The accumulated shedded reactive power in the microgrid
    sections : Section
        The sections in the microgrid
    history : dict
        Dictionary containing the history variables of the network
    monte_carlo_history : dict
        Dictionary containing the history variables from the monte carlo simulation

    Methods
    ----------
    add_connected_line(connected_line, mode)
        Sets the line connecting the microgrid to overlying network
    add_bus(bus)
        Adding a bus including elements on the bus (battery, generation unit, EV park) to the microgrid
    add_buses(buses)
        Adding buses to the microgrid
    add_line(line)
        Adding a line including elements on the line (sensor, circuit breaker, disconnector) to the microgrid
    add_lines(lines)
        Adding lines to the microgrid
    get_lines()
        Returns the lines in the microgrid
    connect(self)
        Connects the microgrid to the parent distribution network by closing the disconnectors on the microgrid lines
    disconnect()
         Disconnects the microgrid from the parent distribution network by opening the disconnectors on the microgrid lines
    reset_slack_bus()
        Resets the slack bus attribute of the buses in the microgrid
    get_max_load()
        Get the maximum load of the microgrid form the entire load history and returns the max load
    get_monte_carlo_history(attribute)
        Returns the specified history variable from the Monte Carlo simulation
    get_history(attribute)
        Returns the specified history variable
    get_system_load()
        Returns the system load in the microgrid at the current time in MW and MVar
    reset_energy_shed_variables()
        Resets the energy.shed variables

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
        Microgrid.counter += 1
        self.name = "microgrid{:d}".format(Microgrid.counter)
        self.mode = mode

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
        self.controller = MicrogridController(
            name=self.name + "_controller",
            power_network=self,
        )
        self.comp_list = list()
        self.comp_dict = dict()

        # PowerNetwork connections
        self.distribution_network = distribution_network
        self.distribution_network.add_child_network(self)
        self.distribution_network.power_system.controller.add_microgrid_controller(
            self.controller
        )
        self.distribution_network.power_system.comp_dict[
            self.controller.name
        ] = self.controller
        self.distribution_network.power_system.comp_list.append(
            self.controller
        )

        self.failed_line = False

        self.connected_line = None
        self.circuitbreaker = None
        self.add_connected_line(connected_line, mode)

        # Load shedding
        self.p_energy_shed = 0
        self.acc_p_energy_shed = 0
        self.q_energy_shed = 0
        self.acc_q_energy_shed = 0
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

    def add_connected_line(self, connected_line, mode):
        """
        Sets the line connecting the microgrid to overlying network

        Parameters
        ----------
        connected_line : Line
            The line connecting the distribution system to overlaying network
        mode : str
            Which mode the microgrid follows

        Returns
        ----------
        None

        """
        # Sets the connected line for the microgrid
        self.connected_line = connected_line

        # Add the components attached to the line
        # to the microgrid:

        # CircuitBreaker
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
        self.comp_list.append(self.circuitbreaker)

        # Line
        self.add_line(connected_line)

    def add_bus(self, bus: Bus):
        """
        Adding a bus including elements on the bus (battery, generation unit, EV park) to the microgrid

        Parameters
        ----------
        bus : Bus
            A Bus element

        Returns
        ----------
        None

        """

        # Add bus to microgrid
        self.comp_dict[bus.name] = bus
        bus.handle.color = self.color
        bus.color = self.color
        bus.parent_network = self
        self.buses.append(bus)
        self.buses = unique(self.buses)

        # Add components attached to bus to microgrid:

        # EV-Park
        if bus.ev_park is not None:
            self.comp_dict[bus.ev_park.name] = bus.ev_park
            self.comp_list.append(bus.ev_park)
            self.ev_parks.append(bus.ev_park)
            self.ev_parks = unique(self.ev_parks)

        # Battery
        if bus.battery is not None:
            # Set microgrid mode
            bus.battery.set_mode(self.mode)
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
        self.distribution_network.power_system.add_bus(bus)

    def add_buses(self, buses: list):
        """
        Adding buses to the microgrid

        Parameters
        ----------
        buses : list
            A list of Bus elements in the microgrid

        Returns
        ----------
        None

        """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding a line and the components connected to the line to the microgrid

        Parameters
        ----------
        line : Line
            A Line element

        Returns
        ----------
        None

        """

        # Add line to microgrid
        line.handle.color = self.color
        line.color = self.color
        self.lines.append(line)
        self.lines = unique(self.lines)

        # Add components attached to bus to microgrid:

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

        # Set microgrid as parent network
        line.add_parent_network(self)

        # Add line to power system
        self.distribution_network.power_system.add_line(line)

    def add_lines(self, lines: list):
        """
        Adding lines to the microgrid

        Parameters
        ----------
        lines : list
            A list of Line elements in the microgrid

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
            List of Line elements

        """
        return self.lines

    def connect(self):
        """
        Connects the microgrid to the parent distribution network by closing the disconnectors on the microgrid lines


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
        Disconnects the microgrid from the parent distribution network by opening the disconnectors on the microgrid lines

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
        Get the maximum load of the microgrid for the entire load history and returns the max load

        Parameters
        ----------
        None

        Returns
        ----------
        p_load_max : float
            The maximum active power load of the microgrid for the entire loading history

        q_load_max : float
            The maximum reactive power load of the microgrid for the entire loading history

        """
        p_load_max, q_load_max = 0, 0
        for bus in self.buses:
            if bus.pload_data != list():
                d_bus = bus  # Dummy bus used to find number of increments
                n_increments = len(d_bus.pload_data[0])  # Number of increments
                break
        for increment in range(n_increments):
            p_load, q_load = 0, 0
            for bus in self.buses:
                for i in range(len(bus.pload_data)):
                    p_load += bus.pload_data[i][increment] * bus.n_customers
                    q_load += bus.qload_data[i][increment] * bus.n_customers
            p_load_max = max(p_load_max, p_load)
            q_load_max = max(q_load_max, q_load)
        return p_load_max, q_load_max

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable from the Monte Carlo simulation

        Parameters
        ----------
        attribute : str
            Microgrid attribute

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
            Microgrid attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def get_system_load(self):
        """
        Returns the system load in the microgrid at the current time in MW and MVar

        Parameters
        ----------
        None

        Returns
        ----------
        pload : float
            The active power load in the microgrid
        qload : float
            The reactive power load in the microgrid

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
