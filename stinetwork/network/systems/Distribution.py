from stinetwork.network.components import Bus, Line
from .Network import Network
from .Transmission import Transmission


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

        self.buses = list()
        self.lines = list()
        self.comp_dict = dict()
        self.parent_network = transmission_network
        transmission_network.add_child_network(self)
        self.power_system = transmission_network.parent_network
        self.child_network_list = list()

        self.failed_line = False

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
        for discon in c_b.disconnectors:
            self.comp_dict[discon.name] = discon
        self.add_line(connected_line)

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

    def SAIFI(self):
        """
        Returns the current SAIFI (System average interruption failure index)
        """
        interrupted_customers = sum(
            [bus.interruptions * bus.n_customers for bus in self.buses]
        )
        total_customers = sum([bus.n_customers for bus in self.buses])
        return interrupted_customers / total_customers

    def SAIDI(self):
        """
        Returns the current SAIFI (System average interruption duration index)
        """
        sum_outage_time_x_n_customer = sum(
            [bus.acc_outage_time * bus.n_customers for bus in self.buses]
        )
        total_customers = sum([bus.n_customers for bus in self.buses])
        return sum_outage_time_x_n_customer / total_customers

    def CAIDI(self):
        """
        Returns the current CAIFI (Customer average interruption duration index)
        """
        saifi = self.SAIFI()
        if saifi != 0:
            return self.SAIDI() / saifi
        else:
            return 0

    def EENS(self):
        """
        Returns the current EENS (Expected energy not supplied)
        """
        dt = 1  # Time increment
        sum_outage_time_x_load_shed = sum(
            [dt * bus.acc_p_load_shed for bus in self.buses]
        )
        total_customers = sum([bus.n_customers for bus in self.buses])
        return sum_outage_time_x_load_shed / total_customers


if __name__ == "__main__":
    pass
