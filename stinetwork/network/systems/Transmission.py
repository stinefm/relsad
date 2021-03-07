from stinetwork.network.components import Bus, Line, CircuitBreaker, Disconnector
from .Network import *
from .PowerSystem import *
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.topology.paths import find_backup_lines_between_sub_systems
from stinetwork.visualization.plotting import plot_history, plot_history_last_state, plot_topology
from stinetwork.results.storage import save_history
from stinetwork.utils import unique, subtract
import numpy as np
from scipy.optimize import linprog, OptimizeWarning
import warnings

class Transmission(Network):
    """ Class defining a transmission network type """

    ## Visual attributes
    color="steelblue"

    ## Counter
    counter = 0

    def __init__(self, power_system, bus:Bus):
        """ Initializing transmission network type content 
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

        bus.handle.color = self.color
        bus.color = self.color
        self.parent_network.add_bus(bus)

        bus.set_slack()
        self.slack_bus = bus

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Transmission(name={self.name})'

    def __eq__(self,other):
        try:
            return self.name == other.name
        except:
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

    def add_bus(self, bus:Bus):
        pass

    def add_buses(self, buses:list):
        pass

    def add_line(self, line:Line):
        pass

    def add_lines(self, lines:list):
        pass

    def get_lines(self):
        """
        Returns the lines in the transmission network
        """
        return None

if __name__=="__main__":
    pass
