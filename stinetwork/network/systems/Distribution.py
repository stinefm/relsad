from stinetwork.network.components import Bus, Line, CircuitBreaker, Disconnector
from .Network import *
from .Transmission import *
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.topology.paths import find_backup_lines_between_sub_systems
from stinetwork.visualization.plotting import plot_history, plot_history_last_state, plot_topology
from stinetwork.results.storage import save_history
from stinetwork.utils import unique, subtract
import numpy as np
from scipy.optimize import linprog, OptimizeWarning
import warnings

class Distribution(Network):
    """ Class defining a distribution network type """

    ## Visual attributes
    color="steelblue"

    ## Counter
    counter = 0

    def __init__(self, transmission_network:Transmission, connected_line:Line):
        """ Initializing distributed network type content
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

        self.connected_line = connected_line
        c_b = connected_line.circuitbreaker
        if self.connected_line.circuitbreaker is None:
            raise Exception("{} connects the distribution network to the " \
                            "transmission network, it must contain a circuitbreaker".format(connected_line))
        self.comp_dict[c_b.name] = c_b
        for discon in c_b.disconnectors:
            self.comp_dict[discon.name] = discon
        self.add_line(connected_line)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Distribution(name={self.name})'

    def __eq__(self,other):
        try:
            return self.name == other.name
        except:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus:Bus):
        """ Adding bus to distribution
            Input: bus(Bus) """
        self.comp_dict[bus.name] = bus
        bus.handle.color = self.color
        bus.color = self.color
        bus.parent_network = self
        self.buses.append(bus)
        self.power_system.add_bus(bus)

    def add_buses(self,buses:set):
        """ Adding buses to distribution
            Input: buses(list(Bus)) """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line:Line):
        """ Adding line to distribution
            Input: line(Line) """
        line.handle.color = self.color
        line.color = self.color
        self.comp_dict[line.name] = line
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
        self.lines.append(line)
        line.add_parent_network(self)
        self.power_system.add_line(line)

    def add_lines(self, lines:set):
        """ Adding lines to distribution
            Input: lines(list(Line)) """
        for line in lines:
            self.add_line(line)

    def get_lines(self):
        """
        Returns the lines in the distribution network
        """
        return self.lines

    def reset_slack_bus(self):
        """
        Resets the slack bus attribute of the buses in the distribution network
        """
        for bus in self.buses:
            bus.is_slack = False

    def add_child_network(self, network):
        """
        Adds child network
        """
        self.child_network_list.append(network)
        self.parent_network.add_child_network(network)

if __name__=="__main__":
    pass
