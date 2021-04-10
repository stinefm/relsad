from stinetwork.network.components import Bus, Line
from .Network import Network
from .Distribution import Distribution


class Microgrid(Network):
    """ Class defining a microgrid network type """

    ## Visual attributes
    color = "seagreen"

    ## Counter
    counter = 0

    def __init__(
        self,
        distribution_network: Distribution,
        connected_line: Line,
        mode: int = 2,
    ):
        """Initializing microgrid network type content
        Content:
            mode(int): Microgrid mode, 1) Survival, 2) Full support, 3) Limited support

            buses(list): List of buses
            lines(list): List of lines
            comp_dict(dict): Dictionary of components
            connected_line(Line): Line connected to distrubution network
        """
        Microgrid.counter += 1
        self.name = "microgrid{:d}".format(Microgrid.counter)

        self.mode = mode

        self.buses = list()
        self.lines = list()
        self.comp_dict = dict()
        self.distribution_network = distribution_network
        self.distribution_network.add_child_network(self)
        self.child_network_list = None

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
        """Adding bus to microgrid
        Input: bus(Bus)"""
        if bus.get_battery() is not None:
            bus.get_battery().set_mode(self.mode)
        self.comp_dict[bus.name] = bus
        bus.handle.color = self.color
        bus.color = self.color
        bus.parent_network = self
        self.buses.append(bus)
        self.distribution_network.power_system.add_bus(bus)

    def add_buses(self, buses: list):
        """Adding buses to microgrid
        Input: buses(list(Bus))"""
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """Adding line to microgrid
        Input: line(Line)"""
        line.handle.color = self.color
        line.color = self.color
        self.comp_dict[line.name] = line
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
        self.lines.append(line)
        line.add_parent_network(self)
        self.distribution_network.power_system.add_line(line)

    def add_lines(self, lines: list):
        """Adding lines to microgrid
        Input: lines(list(Line))"""
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the microgrid
        """
        return self.lines

    def connect(self):
        """
        Connects microgrid to parent distribution network by closing the
        disconnectors on the microgrid lines
        """
        for discon in self.connected_line.get_disconnectors():
            if discon.is_open:
                discon.close()

    def disconnect(self):
        """
        Disconnects microgrid to parent distribution network by opening the
        disconnectors on the microgrid lines
        """
        for discon in self.connected_line.get_disconnectors():
            if not discon.is_open:
                discon.open()

    def reset_slack_bus(self):
        """
        Resets the slack bus attribute of the buses in the microgrid
        """
        for bus in self.buses:
            bus.is_slack = False

    def get_max_load(self):
        max_load = 0
        for bus in self.buses:
            for load_type in bus.load_dict:
                max_load = max(
                    max_load, max(bus.load_dict[load_type]["pload"].flatten())
                )
        return max_load


if __name__ == "__main__":
    pass
