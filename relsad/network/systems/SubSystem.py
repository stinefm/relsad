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
    INF,
)
from relsad.Time import (
    Time,
    TimeUnit,
    TimeStamp,
)


class SubSystem:
    """ Class defining a sub system network type 
    ...

    Attributes
    ----------
    name : str
        Name of the sub system
    slack
    buses : list
        List of all buses in the sub system
    ev_parks : list
        List of all EV parks in the sub system
    batteries : list 
        List of all batteries in the sub system
    production : list
        List of all generation units in the sub system
    lines : list 
        List of all lines in the sub system
    sensors : list 
        List of all sensors in the sub system 
    circuitbreaker : list
        List of all circuit breakers in the sub system
    disconnectors : list
        List of all disconnectors in the sub system
    intelligent_switch : list
        List of all intelligent switches in the sub system
    comp_list : list
        List containing the components in the sub system
    comp_dict : dict
        Dictionary containing the components in the sub system
    child_network_list : list
        List containing the child networks to the sub system


    Methods
    ----------
    add_bus(bus)
        Adding a bus including elements on the bus (battery, generation unit, EV parkt) to the sub system

    get()
        Returns the bus representing the overlying network (transmission network)
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
    reset_load_shed_variables()
        Resets the load shed variables   

    """

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
        self.ev_parks = list()
        self.batteries = list()
        self.productions = list()
        self.lines = list()
        self.sensors = list()
        self.intelligent_switch = list()
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
        Adding a bus including elements on the bus (battery, generation unit, EV parkt) to the sub system
 
        Paramters
        ----------
        bus : Bus 
            A bus element

        Returns
        ----------
        None

        """
        self.comp_dict[bus.name] = bus
        self.comp_list.append(bus)
        self.buses.append(bus)
        self.buses = unique(self.buses)
        if bus.ev_park is not None:
            self.comp_dict[bus.ev_park.name] = bus.ev_park
            self.comp_list.append(bus.ev_park)
            self.ev_parks.append(bus.ev_park)
            self.ev_parks = unique(self.ev_parks)
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
                        system_load_balance_p = -INF
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

    def update_ev_parks(
        self,
        fail_duration: Time,
        dt: Time,
        start_time: TimeStamp,
        curr_time: Time,
    ):
        """
        Updates the EV parks in the power system
        """
        hour_of_day = start_time.get_hour_of_day(curr_time)
        p, q = self.get_system_load_balance()
        for ev_park in self.ev_parks:
            p, q = ev_park.update(p, q, fail_duration, dt, hour_of_day)

    def reset_load_flow_data(self):
        """
        Reset the variables used in the load flow analysis
        """
        for bus in self.buses:
            bus.reset_load_flow_data()
        for line in self.lines:
            line.reset_load_flow_data()
