"""
Module containing the system definition of the package
"""

from stinetwork.network.components import Bus, Line, CircuitBreaker, Disconnector
from stinetwork.loadflow.ac import DistLoadFlow
from stinetwork.topology.paths import find_backup_lines_between_sub_systems
from stinetwork.visualization.plotting import plot_history, plot_topology
from stinetwork.results.storage import save_history
import numpy as np
from scipy.optimize import linprog, OptimizeWarning
import warnings


class PowerSystem:

    ## Visual attributes
    color="black"

    ## Counter
    counter = 0

    ## Load shed configurations
    shed_configs = set()

    ## Load shedding
    p_load_shed = 0
    q_load_shed = 0

    ## History
    all_comp_set = set()
    all_buses = set()
    all_batteries = set()
    all_productions = set()
    all_lines = set()
    history = {"p_load_shed":dict(), "q_load_shed":dict()}

    def __init__(self):
        """ Initializing power system content
            Content:
                buses(set): Set of buses
                lines(set): Set of lines
                comp_dict(dict): Dictionary of components
        """
        PowerSystem.counter += 1
        self.name = "ps{:d}".format(PowerSystem.counter)

        self.slack = None

        self.sub_systems = set()

        self.buses = set()
        self.batteries = set()
        self.productions = set()
        self.lines = set()

        self.comp_set = set()
        self.comp_dict = dict()

        self.child_network_set = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'PowerSystem(name={self.name})'

    def __eq__(self,other):
        try:
            return self.buses.union(self.lines)==other.buses.union(other.lines)
        except:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus:Bus):
        """
        Adding bus to power system
        Input: bus(Bus)
        """
        self.comp_dict[bus.name] = bus
        self.comp_set.add(bus)
        PowerSystem.all_comp_set.add(bus)
        self.buses.add(bus)
        PowerSystem.all_buses.add(bus)
        if bus.battery is not None:
            self.comp_dict[bus.battery.name] = bus.battery
            self.comp_set.add(bus.battery)
            self.batteries.add(bus.battery)
            PowerSystem.all_comp_set.add(bus.battery)
            PowerSystem.all_batteries.add(bus.battery)
        if bus.prod is not None:
            self.comp_dict[bus.prod.name] = bus.prod
            self.comp_set.add(bus.prod)
            self.productions.add(bus.prod)
            PowerSystem.all_comp_set.add(bus.prod)
            PowerSystem.all_productions.add(bus.prod)

    def add_buses(self,buses:set):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.add_bus(bus)

    def add_line(self, line:Line):
        """
        Adding line to power system
        Input: line(Line)
        """
        self.comp_dict[line.name] = line
        self.comp_set.add(line)
        PowerSystem.all_comp_set.add(line)
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
            self.comp_set.add(discon)
            PowerSystem.all_comp_set.add(discon)
        if line.circuitbreaker != None:
            c_b = line.circuitbreaker
            self.comp_dict[c_b.name] = c_b
            self.comp_set.add(c_b)
            PowerSystem.all_comp_set.add(c_b)
            for discon in c_b.disconnectors:
                self.comp_dict[discon.name] = discon
                self.comp_set.add(discon)
                PowerSystem.all_comp_set.add(discon)
        self.lines.add(line)
        PowerSystem.all_lines.add(line)

    def add_lines(self, lines:set):
        """ Adding lines to power system
            Input: lines(list(Line)) """
        for line in lines:
            self.add_line(line)

    def get_comp(self, name:str):
        """
        Returns component based on given name
        """
        try:
            return self.comp_dict[name]
        except KeyError:
            print(name)
            print("Component is not part of the network")
            exit()

    def get_comp_set(self):
        """
        Returns set of the components in the power system
        """
        return self.comp_set

    def add_child_network(self, network):
        """
        Adding child network to power system
        """
        self.child_network_set.add(network)

    def reset_slack_bus(self):
        """
        Resets the slack bus of the child networks
        """
        for trans_network in self.trans_network_set:
            trans_network.reset_slack_bus()
        for dist_network in self.dist_network_set:
            dist_network.reset_slack_bus()
        for microgrid in self.microgrid_network_set:
            microgrid.reset_slack_bus()

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

    def shed_active_loads(self):
        """
        Sheds the unsupplied active loads of the power system using a linear minimization
        problem solved with linear programming
        """

        if len(self.sub_systems) <= 1:
            buses = list(self.buses)
            cost = [x.get_cost() for x in buses]
            lines = [x for x in self.lines if x.connected]
            N_D = len(buses)
            N_L = len(lines)
            c = cost+[0]*N_L+[0]*N_D
            A = np.zeros((N_D,N_D+N_L+N_D))
            p_b = list() # Active bus load
            p_gen = list() # Active bus generation
            # Building A-matrix
            for j, bus in enumerate(buses):
                A[j,j] = 1 # lambda_md
                A[j,N_D+N_L+j] = 1 # mu_md
                for line in bus.connected_lines:
                    if line.connected:
                        index = lines.index(line)
                        if bus == line.fbus:
                            A[j,N_D + index] = -1
                        else:
                            A[j,N_D + index] = 1
                p_b.append(max(0,bus.pload))
                flag = False
                for child_network in self.child_network_set:
                    if type(child_network) == Transmission:
                        if bus == child_network.get():
                            p_gen.append(np.inf)
                            flag = True
                if flag == False:
                    p_gen.append(max(0,bus.pprod))
            p_bounds = list()
            for n in range(N_D+N_L+N_D):
                if n < N_D:
                    p_bounds.append((0, p_b[n]))
                elif n >= N_D and n < N_D+N_L:
                    line = lines[n-N_D]
                    l_index = lines.index(line)
                    max_available_flow = line.get_line_load()[0]
                    PL_max = min(line.capacity, abs(max_available_flow))
                    p_bounds.append((-PL_max, PL_max))
                else:
                    p_bounds.append((0,p_gen[n-(N_D+N_L)]))

            f = False
            with warnings.catch_warnings():
                
                warnings.simplefilter("error", OptimizeWarning)
                try:
                    p_res = linprog(c, A_eq=A, b_eq=p_b, bounds=p_bounds, method='simplex', options={"tol":1E-10})

                    if p_res.fun > 0:
                        for i, bus in enumerate(buses):
                            bus.p_load_shed_stack += p_res.x[i]
                        if len(PowerSystem.shed_configs)==0:
                            PowerSystem.shed_configs.add(self)
                        add = True
                        for shed_config in PowerSystem.shed_configs:
                            if self == shed_config:
                                add = False
                                break
                        if add:
                            PowerSystem.shed_configs.add(self)

                except OptimizeWarning:
                    # f = True
                    # print(buses,lines)
                    # self.print_status()

                    # print('c:\n', c)
                    # print('A_eq:\n', A)
                    # print("Active:\n")
                    # print('b_eq:\n', p_b)
                    # print('Bounds:\n', p_bounds)
                    # #print('Results:', p_res)
                    # fig = plot_topology(list(self.buses),list(self.lines))
                    # fig.show()
                    # try:
                    #     input("Press enter to continue")
                    # except SyntaxError:
                    #     pass
                    pass
            if f:
                p_res = linprog(c, A_eq=A, b_eq=p_b, bounds=p_bounds, method='simplex', options={"tol":1E-10})
                if p_res.fun > 0:

                    print(buses,lines)
                    self.print_status()
                    print("Active:\n")
                    print('c:\n', c)
                    print('A_eq:\n', A)
                    print('b_eq:\n', p_b)
                    print('Bounds:\n', p_bounds)
                    print('Results:', p_res)

                    fig = plot_topology(buses,lines)
                    fig.show()

                    try:
                        input("Press enter to continue")
                    except SyntaxError:
                        pass
                    
        else:
            raise Exception("More than one sub system")

    def shed_reactive_loads(self):
        """
        Sheds the unsupplied reactive loads of the power system using a linear minimization
        problem solved with linear programming
        """

        if len(self.sub_systems) <= 1:
            buses = list(self.buses)
            cost = [x.get_cost() for x in buses]
            lines = [x for x in self.lines if x.connected]
            N_D = len(buses)
            N_L = len(lines)
            c = cost+[0]*N_L+[0]*N_D
            A = np.zeros((N_D,N_D+N_L+N_D))
            q_b = list() # Reactive bus load
            q_gen = list() # Reactive bus generation
            # Building A-matrix
            for j, bus in enumerate(buses):
                q_b.append(max(0,bus.qload))
                flag = False
                for child_network in self.child_network_set:
                    if type(child_network) == Transmission:
                        if bus == child_network.get():
                            q_gen.append(np.inf)
                            flag = True
                if flag == False:
                    q_gen.append(max(0,bus.qprod))
            q_bounds = list()
            for n in range(N_D+N_L+N_D):
                if n < N_D:
                    q_bounds.append((0, q_b[n]))
                elif n >= N_D and n < N_D+N_L:
                    line = lines[n-N_D]
                    l_index = lines.index(line)
                    max_available_flow = line.get_line_load()[1]
                    PL_max = min(line.capacity, abs(max_available_flow))
                    q_bounds.append((-PL_max, PL_max))
                else:
                    q_bounds.append((0,q_gen[n-(N_D+N_L)]))
            f = False
            with warnings.catch_warnings():
                
                warnings.simplefilter("error", OptimizeWarning)
                try:
                    q_res = linprog(c, A_eq=A, b_eq=q_b, bounds=q_bounds, method='simplex', options={"tol":1E-10})
                    if q_res.fun > 0:
                        for i, bus in enumerate(buses):
                            bus.q_load_shed_stack += q_res.x[i]
                        if len(PowerSystem.shed_configs)==0:
                            PowerSystem.shed_configs.add(self)
                        add = True
                        for shed_config in PowerSystem.shed_configs:
                            if self == shed_config:
                                add = False
                                break
                        if add:
                            PowerSystem.shed_configs.add(self)

                except OptimizeWarning:
                    # f = True
                    # print(buses,lines)
                    # self.print_status()

                    # print('c:\n', c)
                    # print('A_eq:\n', A)
                    # print("Reactive:\n")
                    # print('b_eq:\n', q_b)
                    # print('Bounds:\n', q_bounds)
                    # #print('Results:', q_res)
                    # fig = plot_topology(list(self.buses),list(self.lines))
                    # fig.show()
                    # try:
                    #     input("Press enter to continue")
                    # except SyntaxError:
                    #     pass
                    pass
            if f:
                q_res = linprog(c, A_eq=A, b_eq=q_b, bounds=q_bounds, method='simplex', options={"tol":1E-10})
                if q_res.fun > 0:

                    print(buses,lines)
                    self.print_status()
                    print('c:\n', c)
                    print('A_eq:\n', A)
                    print("Reactive:\n")
                    print('b_eq:\n', q_b)
                    print('Bounds:\n', q_bounds)
                    print('Results:', q_res)

                    fig = plot_topology(buses,lines)
                    fig.show()

                    try:
                        input("Press enter to continue")
                    except SyntaxError:
                        pass
                    
        else:
            raise Exception("More than one sub system")

    def get_system_load_balance(self):
        """
        Returns the load balance of the system
        """
        system_load_balance_p, system_load_balance_q = 0,0
        for bus in self.buses:
            for child_network in self.child_network_set:
                if type(child_network) == Transmission:
                    if bus == child_network.get():
                        system_load_balance_p = -np.inf
                        system_load_balance_q = 0
                        return system_load_balance_p, system_load_balance_q
            system_load_balance_p += bus.pload - bus.pprod
            system_load_balance_q += bus.qload - bus.qprod
        return system_load_balance_p, system_load_balance_q

    def update_batteries(self):
        """
        Updates the batteries in the power system
        """
        p, q = self.get_system_load_balance()
        for battery in self.batteries:
            p, q = battery.update_bus_load_and_prod(p,q)

    def plot_bus_history(self, save_dir:str):
        """
        Plots the history of the buses in the power system
        """
        plot_history(self.buses, "pload", save_dir)
        plot_history(self.buses, "qload", save_dir)
        plot_history(self.buses, "pprod", save_dir)
        plot_history(self.buses, "qprod", save_dir)
        plot_history(self.buses, "remaining_outage_time", save_dir)
        plot_history(self.buses, "trafo_failed", save_dir)
        plot_history(self.buses, "p_load_shed_stack", save_dir)
        plot_history(self.buses, "q_load_shed_stack", save_dir)

    def save_bus_history(self, save_dir:str):
        """
        saves the history of the buses in the power system
        """
        save_history(self.buses, "pload", save_dir)
        save_history(self.buses, "qload", save_dir)
        save_history(self.buses, "pprod", save_dir)
        save_history(self.buses, "qprod", save_dir)
        save_history(self.buses, "remaining_outage_time", save_dir)
        save_history(self.buses, "trafo_failed", save_dir)
        save_history(self.buses, "p_load_shed_stack", save_dir)
        save_history(self.buses, "q_load_shed_stack", save_dir)

    def plot_battery_history(self, save_dir:str):
        """
        Plots the history of the battery in the power system
        """
        plot_history(self.batteries, "SOC", save_dir)

    def save_battery_history(self, save_dir:str):
        """
        Saves the history of the battery in the power system
        """
        save_history(self.batteries, "SOC", save_dir)

    def plot_load_shed_history(self, save_dir:str):
        """
        Plots the history of the load shedding in the power system
        """
        plot_history([self], "p_load_shed", save_dir)
        plot_history([self], "q_load_shed", save_dir)

    def save_load_shed_history(self, save_dir:str):
        """
        Saves the history of the load shedding in the power system
        """
        save_history([self], "p_load_shed", save_dir)
        save_history([self], "q_load_shed", save_dir)

    def plot_line_history(self, save_dir:str):
        """
        Plots the history of the line in the power system
        """
        plot_history(self.lines, "p_from", save_dir)
        plot_history(self.lines, "q_from", save_dir)
        plot_history(self.lines, "p_to", save_dir)
        plot_history(self.lines, "q_to", save_dir)
        plot_history(self.lines, "remaining_outage_time", save_dir)
        plot_history(self.lines, "failed", save_dir)

    def save_line_history(self, save_dir:str):
        """
        Saves the history of the line in the power system
        """
        save_history(self.lines, "p_from", save_dir)
        save_history(self.lines, "q_from", save_dir)
        save_history(self.lines, "p_to", save_dir)
        save_history(self.lines, "q_to", save_dir)
        save_history(self.lines, "remaining_outage_time", save_dir)
        save_history(self.lines, "failed", save_dir)

    def plot_circuitbreaker_history(self, save_dir:str):
        """
        Plots the history of the circuitbreakers in the power system
        """
        plot_history([x for x in self.comp_set if type(x) == CircuitBreaker], "is_open", save_dir)
        plot_history([x for x in self.comp_set if type(x) == CircuitBreaker], "remaining_section_time", save_dir)
        plot_history([x for x in self.comp_set if type(x) == CircuitBreaker], "prev_section_hour", save_dir)

    def save_circuitbreaker_history(self, save_dir:str):
        """
        Saves the history of the circuitbreakers in the power system
        """
        save_history([x for x in self.comp_set if type(x) == CircuitBreaker], "is_open", save_dir)
        save_history([x for x in self.comp_set if type(x) == CircuitBreaker], "remaining_section_time", save_dir)
        save_history([x for x in self.comp_set if type(x) == CircuitBreaker], "prev_section_hour", save_dir)

    def plot_disconnector_history(self, save_dir:str):
        """
        Plots the history of the disconnectors in the power system
        """
        plot_history([x for x in self.comp_set if type(x) == Disconnector], "is_open", save_dir)

    def save_disconnector_history(self, save_dir:str):
        """
        Saves the history of the disconnectors in the power system
        """
        save_history([x for x in self.comp_set if type(x) == Disconnector], "is_open", save_dir)

    def update_history(self, hour):
        """
        Updates the history variables in the power system
        """
        for bus in PowerSystem.all_buses:
            PowerSystem.p_load_shed += bus.p_load_shed_stack
            PowerSystem.q_load_shed += bus.q_load_shed_stack
        PowerSystem.history["p_load_shed"][hour] = PowerSystem.p_load_shed
        PowerSystem.history["q_load_shed"][hour] = PowerSystem.q_load_shed
        PowerSystem.p_load_shed = 0
        PowerSystem.q_load_shed = 0
        for comp in PowerSystem.all_comp_set:
            comp.update_history(hour)
        for bus in PowerSystem.all_buses:
            bus.reset_load_and_prod_attributes()

    def get_history(self, attribute):
        """
        Returns the specified history variable
        """
        return PowerSystem.history[attribute]

    def run(self, hour):
        """
        Runs power system at current state
        """
        ## Set fail status
        for comp in self.get_comp_set():
            comp.update_fail_status(hour)

        ## Find sub systems
        find_sub_systems(self)
        update_sub_system_slack(self)

        ## Load flow
        for sub_system in self.sub_systems:
            ## Update batteries and history
            sub_system.update_batteries()
            ## Run load flow     
            _sub_buses = DistLoadFlow(list(sub_system.buses),list(sub_system.lines))
            ## Shed load
            sub_system.shed_active_loads()
            sub_system.shed_reactive_loads()
        ## Log results
        self.update_history(hour)


class Transmission:
    """ Class defining a transmission network type """

    ## Visual attributes
    color="steelblue"

    ## Counter
    counter = 0

    def __init__(self, power_system:PowerSystem, bus:Bus):
        """ Initializing transmission network type content 
            Content:
                bus(Bus): Bus
        """
        Transmission.counter += 1
        self.name = "trans_network{:d}".format(Transmission.counter)

        self.parent_network = power_system
        power_system.add_child_network(self)
        self.child_network_set = set()

        self.bus = bus
        self.buses = {bus}

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
        self.child_network_set.add(network)
        self.parent_network.add_child_network(network)

class Distribution:
    """ Class defining a distribution network type """

    ## Visual attributes
    color="steelblue"

    ## Counter
    counter = 0

    def __init__(self, transmission_network:Transmission, connected_line:Line):
        """ Initializing distributed network type content
            Content:
                buses(set): Set of buses
                lines(set): Set of lines
                comp_dict(dict): Dictionary of components
                connected_line(Line): Line connected to distrubution network
        """
        Distribution.counter += 1
        self.name = "dist_network{:d}".format(Distribution.counter)

        self.buses = set()
        self.lines = set()
        self.comp_dict = dict()
        self.parent_network = transmission_network
        transmission_network.add_child_network(self)
        self.power_system = transmission_network.parent_network
        self.child_network_set = set()

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
        self.buses.add(bus)
        self.power_system.add_bus(bus)

    def add_buses(self,buses:set):
        """ Adding buses to distribution
            Input: buses(set(Bus)) """
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
        self.lines.add(line)
        line.add_parent_network(self)
        self.power_system.add_line(line)

    def add_lines(self, lines:set):
        """ Adding lines to distribution
            Input: lines(set(Line)) """
        for line in lines:
            self.add_line(line)
        
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
        self.child_network_set.add(network)
        self.parent_network.add_child_network(network)

class Microgrid:
    """ Class defining a microgrid network type """

    ## Visual attributes
    color="seagreen"

    ## Counter
    counter = 0

    def __init__(self, distribution_network:Distribution, connected_line:Line):
        """ Initializing microgrid network type content
            Content:
                buses(set): Set of buses
                lines(set): Set of lines
                comp_dict(dict): Dictionary of components
                connected_line(Line): Line connected to distrubution network
        """
        Microgrid.counter += 1
        self.name = "microgrid{:d}".format(Microgrid.counter)

        self.buses = set()
        self.lines = set()
        self.comp_dict = dict()
        self.distribution_network = distribution_network
        self.distribution_network.add_child_network(self)
        self.child_network_set = None

        self.connected_line = connected_line
        c_b = connected_line.circuitbreaker
        if self.connected_line.circuitbreaker is None:
            raise Exception("{} connects the microgrid to the " \
                            "distribution network, it must contain a circuitbreaker".format(connected_line))
        self.comp_dict[c_b.name] = c_b
        for discon in c_b.disconnectors:
            self.comp_dict[discon.name] = discon
        self.add_line(connected_line)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Microgrid(name={self.name})'

    def __eq__(self,other):
        try:
            return self.name == other.name
        except:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus:Bus):
        """ Adding bus to microgrid
            Input: bus(Bus) """
        self.comp_dict[bus.name] = bus
        bus.handle.color = self.color
        bus.color = self.color
        self.buses.add(bus)
        self.distribution_network.power_system.add_bus(bus)

    def add_buses(self,buses:list):
        """ Adding buses to microgrid
            Input: buses(list(Bus)) """
        for bus in buses:
            self.add_bus(bus)   
    
    def add_line(self, line:Line):
        """ Adding line to microgrid
            Input: line(Line) """
        line.handle.color = self.color
        line.color = self.color
        self.comp_dict[line.name] = line
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
        self.lines.add(line)
        line.add_parent_network(self)
        self.distribution_network.power_system.add_line(line)

    def add_lines(self, lines:list):
        """ Adding lines to microgrid
            Input: lines(list(Line)) """
        for line in lines:
            self.add_line(line)  

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


def find_sub_systems(p_s:PowerSystem):
    """
    Function that find the independent sub systems of the given power system
    and adds them to the sub_systems set of the power system
    """

    p_s.sub_systems = set()
    # Will only include connected lines
    active_lines = {line for line in p_s.lines if line.connected}
    used_buses = set()
    used_lines = set()
    sub_system = PowerSystem()

    def try_to_add_connected_lines(bus):
        for line in bus.connected_lines-used_lines:
            if line.connected:
                sub_system.add_line(line)
                used_lines.add(line)
                if line.tbus == bus:
                    add_bus(line.fbus)
                    try_to_add_connected_lines(line.fbus)
                else:
                    add_bus(line.tbus)
                    try_to_add_connected_lines(line.tbus)

    def add_bus(bus):
        if bus not in used_buses.union(sub_system.buses):
            sub_system.add_bus(bus)
            used_buses.add(bus)
            for child_network in p_s.child_network_set:
                if bus in child_network.buses:
                    sub_system.add_child_network(child_network)
                

    while not (len(used_buses)+len(used_lines))==(len(p_s.buses)+len(active_lines)):
        for bus in p_s.buses:
            if bus not in used_buses.union(sub_system.buses):
                if (len(sub_system.buses)+len(sub_system.lines)) == 0:
                    add_bus(bus)
                    try_to_add_connected_lines(bus)
                    p_s.sub_systems.add(sub_system)
                    sub_system = PowerSystem()

    if len(p_s.sub_systems) > 1:
        update_backup_lines_between_sub_systems(p_s)

def update_backup_lines_between_sub_systems(p_s:PowerSystem):
    """
    Function that updates the backup lines between the sub systems of the
    power system if they exist and are not failed
    """
    update = False
    for s_1 in p_s.sub_systems:
        for s_2 in p_s.sub_systems:
            if s_1 != s_2:
                external_backup_lines = find_backup_lines_between_sub_systems(s_1,s_2)
                for line in external_backup_lines:
                    if not line.connected and not line.failed:
                        for discon in line.get_disconnectors():
                            if discon.is_open:
                                discon.close()
                        update = True
                        break
            if update:
                break
        if update:
            break
    if update:
        find_sub_systems(p_s)

def update_sub_system_slack(p_s:PowerSystem):
    """
    Function that updates the current slack bus of the sub systems of the
    power system
    """
    possible_sub_systems = list(p_s.sub_systems)
    for sub_system in possible_sub_systems:
        sub_system.slack = None
        for bus in sub_system.buses:
            bus.is_slack = False
        if not set_slack(sub_system): # Remove sub system if slack is not found
            p_s.sub_systems.remove(sub_system)

def set_slack(p_s:PowerSystem):
    """
    Function that sets the slack bus of the power system
    """
    ## Transmission network slack buses in sub_system
    for bus in p_s.buses:
        for child_network in p_s.child_network_set:
            if type(child_network) == Transmission:
                if bus == child_network.get():
                    bus.set_slack()
                    p_s.slack = bus
                    return True
    ## Buses with battery
    if p_s.slack is None:
        for bus in p_s.buses:
            if bus.battery is not None:
                bus.set_slack()
                p_s.slack = bus
                return True
    ## Buses with production
    if p_s.slack is None:
        for bus in p_s.buses:
            if bus.prod is not None:
                bus.set_slack()
                p_s.slack = bus
                return True
    ## Delete if no possible slack
    return False

if __name__=="__main__":
    pass
