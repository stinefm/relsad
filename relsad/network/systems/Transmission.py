from relsad.network.components import Bus, Line
from .Network import Network


class Transmission(Network):
    """ Class defining a transmission network type """

    ## Visual attributes
    color = "steelblue"

    ## Counter
    counter = 0

    def __init__(self, power_system, bus: Bus):
        """Initializing transmission network type content
        Content:
            bus(Bus): Bus
        """
        Transmission.counter += 1
        self.name = "trans_network{:d}".format(Transmission.counter)

        self.parent_network = power_system
        power_system.add_child_network(self)
        self.child_network_list = list()

        self.bus = bus
        self.buses = [bus]
        self.sections = list()

        bus.handle.color = self.color
        bus.color = self.color
        self.parent_network.add_bus(bus)

        bus.set_slack()
        self.slack_bus = bus
        power_system.slack = bus
        # Load shedding
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0

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

    def get(self):
        """
        Returns the bus of the transmission network
        """
        return self.bus

    def reset_slack_bus(self):
        """
        Resets the slack bus of the transmission network
        """
        self.bus.set_slack()

    def add_child_network(self, network):
        """
        Adds child network
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
        """
        return None

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
