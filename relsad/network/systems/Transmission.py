from relsad.network.components import Bus, Line

from .PowerNetwork import PowerNetwork


class Transmission(PowerNetwork):
    """Class defining a transmission network type

    ...

    Attributes
    ----------
    name : str
        Name of the transmission system
    parent_network : PowerSystem
        The parent network of the transmission network
    child_network_list : list
        Lists of child networks
    trafo_bus : Bus
        Bus with tranformer connected to distribution network
    buses : list
        List with the buses in the transmission network
    sections : list
        List with the sections in the transmission network
    ev_parks : list
        List with the EV parks in the transmission network
    p_energy_shed : float
        The active power energy.shed in the transmission network
    acc_p_energy_shed : float
        The accumulated active power energy.shedding in the transmission network
    q_energy_shed : float
        The reactive power energy.shed in the transmission network
    acc_q_energy_shed : float
        The accumulated reactive power energy.shedding in the transmission network
    history : dict
        Dictionary containing the history variables of the transmission network
    monte_carlo_history : dict
        Dictionary containing the history variables from the monte carlo simulation



    Methods
    ----------
    get_trafo_bus()
        Returns the bus connecting to the overlying network (transmission network)
    reset_slack_bus()
        Resets the slack bus of the transmission network
    add_chil_network(network)
        Adds child network
    get_lines()
        Returns the lines in the transmission network
    get_monte_carlo_history(attribute)
        Returns the specified history variable from the Monte Carlo simulation
    get_history(attribute)
        Returns the specified history variable
    get_system_load()
        Returns the system load at the current time in MW and MVar
    reset_energy_shed_variables()
        Resets the energy.shed variables

    """

    ## Visual attributes
    color = "steelblue"

    ## Counter
    counter = 0

    def __init__(self, parent_network, trafo_bus: Bus):
        Transmission.counter += 1
        self.name = "trans_network{:d}".format(Transmission.counter)

        self.parent_network = parent_network
        parent_network.add_child_network(self)
        self.child_network_list = list()

        self.trafo_bus = trafo_bus
        self.buses = [trafo_bus]
        self.sections = list()

        self.ev_parks = list()

        trafo_bus.handle.color = self.color
        trafo_bus.color = self.color
        self.parent_network.add_bus(trafo_bus)

        trafo_bus.set_slack()
        parent_network.slack = trafo_bus
        # Load shedding
        self.p_energy_shed = 0
        self.acc_p_energy_shed = 0
        self.q_energy_shed = 0
        self.acc_q_energy_shed = 0

        ## History
        self.history: dict = {}
        self.monte_carlo_history: dict = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Transmission(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def get_trafo_bus(self):
        """
        Returns the bus connecting to the overlying network (transmission network)

        Parameters
        ----------
        None

        Returns
        ----------
        bus : Bus
            The bus connecting the overlying network

        """
        return self.trafo_bus

    def reset_slack_bus(self):
        """
        Resets the slack bus of the transmission network

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.trafo_bus.set_slack()

    def add_child_network(self, network):
        """
        Adds child network

        Parameters
        ----------
        network : PowerNetwork
            A network

        Returns
        ----------
        None

        """
        self.child_network_list.append(network)
        self.parent_network.add_child_network(network)

    def add_bus(self, bus: Bus):
        pass

    def add_buses(self, buses: list):
        pass

    def add_line(self, line: Line):
        pass

    def add_lines(self, lines: list):
        pass

    def get_lines(self):
        """
        Returns the lines in the transmission network

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        return None

    def get_monte_carlo_history(self, attribute):
        """
        Returns the specified history variable

        Parameters
        ----------
        attribute : str
            System attribute

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
            System attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def get_system_load(self):
        """
        Returns the system load at the current time in MW and MVar

        Parameters
        ----------
        None

        Returns
        ----------
        pload : float
            The active power load in the transmission system
        qload : float
            The reactive power load in the tranmission system

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
