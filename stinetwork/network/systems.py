from stinetwork.network.components import Bus, Line, Battery, Disconnector, Production, CircuitBreaker
from stinetwork.topology.paths import find_backup_lines_between_sub_systems
from stinetwork.visualization.plotting import plot_topology, plot_history
import numpy as np
from scipy.optimize import linprog

class PowerSystem:

    ## Visual attributes
    color="black"

    ## Counter
    counter = 0

    ## Load shed configurations
    shed_configs = set()

    ## Load shedding
    load_shed = 0

    ## History
    history = {"load_shed":list()}

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
        self.lines = set()

        self.comp_dict = dict()

        self.dist_network_set = set()
        self.microgrid_network_set = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'PowerSystem(name={self.name})'

    def __eq__(self,other):
        try:
            return self.buses.union(self.lines)==other.buses.union(other.lines)
        except:False

    def __hash__(self):
        return hash(self.name)

    def add_bus(self, bus:Bus):
        self.comp_dict[bus.name] = bus
        self.buses.add(bus)
        if bus.battery != None:
            self.comp_dict[bus.battery.name] = bus.battery
            self.batteries.add(bus.battery)

    def add_buses(self,buses:set):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.add_bus(bus)
            
    def add_line(self, line:Line):
        self.comp_dict[line.name] = line
        for discon in line.disconnectors:
            self.comp_dict[discon.name] = discon
        if line.circuitbreaker != None:
            cb = line.circuitbreaker
            self.comp_dict[cb.name] = cb
            for discon in cb.disconnectors:
                self.comp_dict[discon.name] = discon
        self.lines.add(line)

    def add_lines(self, lines:set):
        """ Adding lines to power system
            Input: lines(list(Line)) """
        for line in lines:
            self.add_line(line)

    def get_comp(self, name:str):
        try:
            return self.comp_dict[name]
        except BaseException:
            print("Component is not part of the network")

    def get_comp_set(self):
        return self.buses.union(self.lines)

    def add_distribution_network(self, dist_network):
        self.dist_network_set.add(dist_network)

    def add_microgrid_network(self, microgrid_network):
        self.microgrid_network_set.add(microgrid_network)

    def reset_slack_bus(self):
        for dist_network in self.dist_network_set:
            dist_network.reset_slack_bus()
        for microgrid in self.microgrid_network_set:
            microgrid.reset_slack_bus()

    def print_status(self):
        print("Buses:")
        for bus in self.buses:
            bus.print_status()
        print("Lines:")
        for line in self.lines:
            line.print_status()

    def shed_loads(self):

        if len(self.sub_systems) <= 1:

            buses = list(self.buses)
            cost = [x.get_cost() for x in buses]
            lines = [x for x in self.lines if x.connected]


            N_D = len(buses)

            N_L = len(lines)

            c = cost+[0]*N_L+[0]*N_D

            A = np.zeros((N_D,N_D+N_L+N_D))

            b = list() # Bus load
            gen = list() # Bus generation

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

                b.append(max(0,bus.pload))

                flag = False
                for dist_network in self.dist_network_set:
                    if bus == dist_network.get_slack_bus():
                        gen.append(np.inf)
                        flag = True
                if flag == False:
                    gen.append(max(0,bus.pprod))

            bounds = list()
            for n in range(N_D+N_L+N_D):
                if n < N_D:
                    bounds.append((0, b[n]))
                elif n >= N_D and n < N_D+N_L:
                    line = lines[n-N_D]
                    l_index = lines.index(line)
                    max_available_flow = line.get_line_load()[0]

                    PL_max = min(line.capacity, abs(max_available_flow))
                    bounds.append((-PL_max, PL_max))
                else:
                    bounds.append((0,gen[n-(N_D+N_L)]))

            res = linprog(c, A_eq=A, b_eq=b, bounds=bounds, method='simplex', options={"tol":1E-10})

            if res.fun > 0:
                PowerSystem.load_shed += sum(res.x[0:N_D])
                if len(PowerSystem.shed_configs)==0:
                    PowerSystem.shed_configs.add(self)
                add = True
                for shed_config in PowerSystem.shed_configs:
                    if self == shed_config:
                        add = False
                        break
                if add:
                    PowerSystem.shed_configs.add(self)

                # print(buses,lines)
                # self.print_status()

                # print('c:\n', c)
                # print('A_eq:\n', A)
                # print('b_eq:\n', b)
                # print('Bounds:\n', bounds)
                # print('Results:', res)
                # fig = plot_topology(list(self.buses),list(self.lines))
                # fig.show()
                # try:
                #     input("Press enter to continue")
                # except SyntaxError:
                #     pass

        else:
            raise(Exception("More than one sub system"))

    def get_system_load_balance(self):
        system_load_balance_p, system_load_balance_q = 0,0
        for bus in self.buses:
            for dist_network in self.dist_network_set:
                if bus == dist_network.get_slack_bus():
                    system_load_balance_p = -np.inf
                    system_load_balance_q = 0
                    return system_load_balance_p, system_load_balance_q
            system_load_balance_p += bus.pload - bus.pprod
            system_load_balance_q += bus.qload - bus.qprod
        return system_load_balance_p, system_load_balance_q

    def update_batteries(self):
        p, q = self.get_system_load_balance()
        for battery in self.batteries:
            p, q = battery.update_bus_load_and_prod(p,q)

    def plot_bus_history(self):
        plot_history(self.buses, "pload")
        plot_history(self.buses, "qload")
        plot_history(self.buses, "pprod")
        plot_history(self.buses, "qprod")

    def plot_battery_history(self):
        plot_history(self.batteries, "SOC")
    
    def plot_load_shed_history(self):
        plot_history([self], "load_shed")        

    def update_history(self):
        PowerSystem.history["load_shed"].append(PowerSystem.load_shed)
        PowerSystem.load_shed = 0
        for bus in self.buses:
            bus.update_history()
            bus.reset_load_and_prod_attributes()
    
    def get_history(self, attribute):
        return PowerSystem.history[attribute]

class Distribution:
    """ Class defining a distribution network type """

    ## Visual attributes
    color="steelblue"

    ## Counter
    counter = 0

    def __init__(self, powerSystem:PowerSystem):
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
        self.powerSystem = powerSystem
        self.slack_bus = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Distribution(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def add_buses(self,buses:set):
        """ Adding buses to power system
            Input: buses(set(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
            bus.handle.color = self.color
            bus.color = self.color
            if bus.is_slack:
                if self.slack_bus == None:
                    self.slack_bus = bus
                else:
                    raise Exception("The distribution network can only have one slack bus")
            self.buses.add(bus)
        self.powerSystem.add_buses(buses)

    def add_lines(self, lines:set):
        """ Adding lines to power system
            Input: lines(set(Line)) """
        for line in lines:
            line.handle.color = self.color
            line.color = self.color
            self.comp_dict[line.name] = line
            for discon in line.disconnectors:
                self.comp_dict[discon.name] = discon
            if line.circuitbreaker != None:
                cb = line.circuitbreaker
                self.comp_dict[cb.name] = cb
                for discon in cb.disconnectors:
                    self.comp_dict[discon.name] = discon
            self.lines.add(line)
        self.powerSystem.add_lines(lines)

    def get_slack_bus(self):
        return self.slack_bus

    def reset_slack_bus(self):
        for bus in self.buses:
            if bus == self.slack_bus:
                bus.set_slack()
            else:
                bus.is_slack = False


class Microgrid:
    """ Class defining a microgrid network type """

    ## Visual attributes
    color="seagreen"

    ## Counter
    counter = 0

    def __init__(self, distibutionNetwork:Distribution, connected_line:Line):
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
        self.distibutionNetwork = distibutionNetwork
        self.connected_line = connected_line
        self.add_lines([connected_line])

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Microgrid(name={self.name})'
    
    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def add_buses(self,buses:list):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
            bus.handle.color = self.color
            bus.color = self.color
            self.buses.add(bus)
        self.distibutionNetwork.powerSystem.add_buses(buses)

    def add_lines(self, lines:list):
        """ Adding lines to power system
            Input: lines(list(Line)) """
        for line in lines:
            line.handle.color = self.color
            line.color = self.color
            self.comp_dict[line.name] = line
            for discon in line.disconnectors:
                self.comp_dict[discon.name] = discon
            if line.circuitbreaker != None:
                cb = line.circuitbreaker
                self.comp_dict[cb.name] = cb
                for discon in cb.disconnectors:
                    self.comp_dict[discon.name] = discon
            self.lines.add(line)
        self.distibutionNetwork.powerSystem.add_lines(lines)

    
    def connect(self):
        self.connected_line.connect()

    def disconnect(self):
        self.connected_line.disconnect()

    def reset_slack_bus(self):
        for bus in self.buses:
            bus.is_slack = False


def find_sub_systems(ps:PowerSystem):

    ps.sub_systems = set()
    active_lines = {line for line in ps.lines if line.connected} # Will only include connected lines
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
            for dist_network in ps.dist_network_set:
                for dist_bus in dist_network.buses:
                    if bus == dist_bus:
                        sub_system.add_distribution_network(dist_network)
                        break    

    while not (len(used_buses)+len(used_lines))==(len(ps.buses)+len(active_lines)):
        for bus in ps.buses:
            if bus not in used_buses.union(sub_system.buses):
                if (len(sub_system.buses)+len(sub_system.lines)) == 0:
                    add_bus(bus)
                    try_to_add_connected_lines(bus)
                    ps.sub_systems.add(sub_system)
                    sub_system = PowerSystem()

    if len(ps.sub_systems) > 1:
        update_backup_lines_between_sub_systems(ps)

def update_backup_lines_between_sub_systems(ps:PowerSystem):
    update = False
    for s1 in ps.sub_systems:
        for s2 in ps.sub_systems:
            if s1 != s2:
                external_backup_lines = find_backup_lines_between_sub_systems(s1,s2)
                for line in external_backup_lines:
                    if not line.connected and not line.failed:
                        line.connect()
                        update = True
                        break
            if update:
                break
        if update:
            break
    if update:
        find_sub_systems(ps)
        
def update_sub_system_slack(ps:PowerSystem):
    possible_sub_systems = list(ps.sub_systems)
    for sub_system in possible_sub_systems:
        sub_system.slack = None
        for bus in sub_system.buses:
            bus.is_slack = False
        if not set_slack(sub_system): # Remove sub system if slack is not found
            ps.sub_systems.remove(sub_system)

def set_slack(ps:PowerSystem):
    ## Distribution network slack buses in sub_system
    for bus in ps.buses:
        for dist_network in ps.dist_network_set:
            if bus == dist_network.get_slack_bus():
                bus.set_slack()
                ps.slack = bus
                return True
    ## Buses with battery
    if ps.slack == None:
        for bus in ps.buses:
            if bus.battery != None:
                bus.set_slack()
                ps.slack = bus
                return True
    ## Buses with production
    if ps.slack == None:
        for bus in ps.buses:
            if bus.prod != None:
                bus.set_slack()
                ps.slack = bus
                return True
    ## Delete if no possible slack
    if ps.slack == None:
        return False

if __name__=="__main__":
    pass
