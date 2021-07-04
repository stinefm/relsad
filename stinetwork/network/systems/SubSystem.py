import numpy as np
from stinetwork.network.components import (
    Bus,
    Line,
)
from stinetwork.network.systems import Network
from .Transmission import Transmission
from stinetwork.utils import eq
from stinetwork.utils import unique


class SubSystem(Network):

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
        # Load shedding
        self.p_load_shed = 0
        self.acc_p_load_shed = 0
        self.q_load_shed = 0
        self.acc_q_load_shed = 0
        # Sub-systems
        self.sub_systems = list()
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
        ## History
        self.history: dict = {}
        self.monte_carlo_history: dict = {}
        ## Random instance
        self.random_instance: np.random.Generator = None

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

    def get_lines(self):
        """
        Returns the lines in the power system
        """
        return self.lines

    def get_comp(self, name: str):
        """
        Returns component based on given name
        """
        try:
            return self.comp_dict[name]
        except KeyError:
            print(name)
            print("Component is not part of the network")
            exit()

    def get_comp_list(self):
        """
        Returns list of the components in the power system
        """
        return self.comp_list

    def add_child_network(self, network):
        """
        Adding child network to power system
        """
        self.child_network_list.append(network)

    def reset_slack_bus(self):
        """
        Resets the slack bus of the child networks
        """
        for child_network in self.child_network_list:
            child_network.reset_slack_bus()

    def print_status(self):
        """
        Prints the status of the buses and lines in the power system
        """
        print("Buses:")
        for bus in self.buses:
            bus.print_status()
        print("Lines:")
        for line in self.lines:
            line.print_status()

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

    def update_batteries(self, fail_duration: int):
        """
        Updates the batteries in the power system
        """
        p, q = self.get_system_load_balance()
        for battery in self.batteries:
            if (
                battery.mode in ["survival", "full support"]
                and fail_duration == 1
            ):
                battery.draw_SOC_state()
            p, q = battery.update_bus_load_and_prod(p, q)

    def update_fail_status(self, curr_time):
        for bus in self.buses:
            bus.update_fail_status(curr_time)
        for line in self.lines:
            line.update_fail_status(curr_time)
        for comp in self.get_comp_list():
            if comp not in self.buses + self.lines:
                comp.update_fail_status(curr_time)

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

    def get_max_load(self):
        """
        Get the maximum load of the power system for the entire loading history in MW/MVar

        Parameters
        ----------
        None

        Returns
        ----------
        p_load_max : float
            The maximum active load of the power system for the entire loading history

        q_load_max : float
            The maximum reactive load of the power system for the entire loading history

        """
        p_load_max, q_load_max = 0, 0
        for bus in self.buses:
            if bus.load_dict != dict():
                d_bus = bus  # Dummy bus used to find number of increments
                n_increments = len(
                    d_bus.load_dict[list(d_bus.load_dict.keys())[0]][
                        "pload"
                    ].flatten()
                )  # Number of increments
                break
        for increment in range(n_increments):
            p_load, q_load = 0, 0
            for bus in self.buses:
                for load_type in bus.load_dict:
                    p_load += (
                        bus.load_dict[load_type]["pload"].flatten()[increment]
                        * bus.n_customers
                    )
                    q_load += (
                        bus.load_dict[load_type]["qload"].flatten()[increment]
                        * bus.n_customers
                    )
            p_load_max = max(p_load_max, p_load)
            q_load_max = max(q_load_max, q_load)
        return p_load_max, q_load_max

    def add_load_dict(self, load_dict: dict):
        for bus in self.buses:
            if bus in load_dict:
                bus.add_load_dict(load_dict[bus])

    def add_prod_dict(self, prod_dict: dict):
        for prod in self.productions:
            if prod in prod_dict:
                prod.add_prod_dict(prod_dict[prod])

    def set_load(self, curr_time):
        for bus in self.buses:
            bus.set_load(curr_time)

    def set_prod(self, curr_time):
        for prod in self.productions:
            prod.set_prod(curr_time)
        for bus in self.buses:
            if bus.battery is not None:
                bus.reset_prod()

    def failed_comp(self):
        """
        Returns True if the power system contains a failed component, and False otherwise
        """
        return any(
            [True if bus.trafo_failed else False for bus in self.buses]
        ) or any([True if line.failed else False for line in self.lines])

    def full_batteries(self):
        """
        Returns True if the batteries of the power system are full, and False otherwise
        """
        return all(
            [
                True if eq(battery.SOC, battery.SOC_max) else False
                for battery in self.batteries
            ]
        )

    def reset_load_flow_data(self):
        """
        Reset the variables used in the load flow analysis
        """
        for bus in self.buses:
            bus.reset_load_flow_data()
        for line in self.lines:
            line.reset_load_flow_data()