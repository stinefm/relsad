import numpy as np
from relsad.network.components import (
    Bus,
    Line,
)
from relsad.network.systems import Network
from .Transmission import Transmission
from relsad.utils import (
    eq,
    unique,
    Time,
    TimeUnit,
)


class SubSystem:

    ## Visual attributes
    color = "black"

    ## Counter
    counter = 0

    def __init__(self):
        """Initializing sub system content
        Content:
            buses(set): List of buses
            lines(set): List of lines
            comp_dict(dict): Dictionary of components
        """
        # Info
        SubSystem.counter += 1
        self.name = "ps{:d}".format(SubSystem.counter)
        # Load flow
        self.slack = None
        # Components
        self.buses = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()
        self.circuitbreakers = list()
        self.disconnectors = list()
        self.comp_list = list()
        self.comp_dict = dict()
        ## Child networks
        self.child_network_list: list = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"SubSystem(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "buses") and hasattr(other, "lines"):
            return set(unique(self.buses + self.lines)) == set(
                unique(other.buses + other.lines)
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus: Bus):
        """
        Adding bus to sub system
        Input: bus(Bus)
        """
        self.comp_dict[bus.name] = bus
        self.comp_list.append(bus)
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
        self.comp_list = unique(self.comp_list)

    def add_buses(self, buses: list):
        """Adding buses to sub system
        Input: buses(list(Bus))"""
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line: Line):
        """
        Adding line to sub system
        Input: line(Line)
        """
        self.comp_dict[line.name] = line
        self.comp_list.append(line)
        self.lines.append(line)
        self.lines = unique(self.lines)
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
            self.comp_list.append(discon)
            self.disconnectors.append(discon)
            self.disconnectors = unique(self.disconnectors)
        if line.circuitbreaker is not None:
            c_b = line.circuitbreaker
            self.comp_dict[c_b.name] = c_b
            self.comp_list.append(c_b)
            self.circuitbreakers.append(c_b)
            self.circuitbreakers = unique(self.circuitbreakers)
            for discon in c_b.disconnectors:
                self.comp_dict[discon.name] = discon
                self.comp_list.append(discon)
                self.disconnectors.append(discon)
                self.disconnectors = unique(self.disconnectors)
        self.comp_list = unique(self.comp_list)

    def add_lines(self, lines: list):
        """Adding lines to power system
        Input: lines(list(Line))"""
        for line in lines:
            self.add_line(line)

    def add_child_network(self, network):
        """
        Adding child network to power system
        """
        self.child_network_list.append(network)

    def get_system_load_balance(self):
        """
        Returns the load balance of the system
        """
        system_load_balance_p, system_load_balance_q = 0, 0
        for bus in self.buses:
            for child_network in self.child_network_list:
                if isinstance(child_network, Transmission):
                    if bus == child_network.get():
                        system_load_balance_p = -np.inf
                        system_load_balance_q = 0
                        return system_load_balance_p, system_load_balance_q
            system_load_balance_p += bus.pload - bus.pprod
            system_load_balance_q += bus.qload - bus.qprod
        return system_load_balance_p, system_load_balance_q

    def update_batteries(self, fail_duration: Time, dt: Time):
        """
        Updates the batteries in the power system
        """
        p, q = self.get_system_load_balance()
        for battery in self.batteries:
            p, q = battery.update(p, q, fail_duration, dt)

    def reset_load_flow_data(self):
        """
        Reset the variables used in the load flow analysis
        """
        for bus in self.buses:
            bus.reset_load_flow_data()
        for line in self.lines:
            line.reset_load_flow_data()
