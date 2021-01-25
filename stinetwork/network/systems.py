from stinetwork.network.components import Bus, Line, Battery, Disconnector, Production, CircuitBreaker
from stinetwork.topology.paths import find_backup_lines_between_sub_systems

class PowerSystem:

    ## Visual attributes
    color="black"

    ## Counter
    counter = 0

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
        self.lines = set()

        self.comp_dict = dict()

        self.dist_network_set = set()
        self.microgrid_network_set = set()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'PowerSystem(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def add_buses(self,buses:set):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
            self.buses.add(bus)

    def add_lines(self, lines:set):
        """ Adding lines to power system
            Input: lines(list(Line)) """
        for line in lines:
            self.comp_dict[line.name] = line
            for discon in line.disconnectors:
                self.comp_dict[discon.name] = discon
            if line.circuitbreaker != None:
                cb = line.circuitbreaker
                self.comp_dict[cb.name] = cb
                for discon in cb.disconnectors:
                    self.comp_dict[discon.name] = discon
            self.lines.add(line)

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
            print("name: {}, trafo_failed={}, pload={:.2f}, is_slack={}, toline={}, fromline={}"\
                    .format(bus.name, bus.trafo_failed, bus.pload, bus.is_slack, bus.toline if bus.toline==None else bus.toline.name, bus.fromline if bus.fromline == None else bus.fromline.name ))
        print("Lines:")
        for line in self.lines:
            print("name: {}, failed={}, connected={}".format(line.name, line.failed, line.connected))


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
                sub_system.lines.add(line)
                used_lines.add(line)
                if line.tbus == bus:
                    add_bus(line.fbus)
                    try_to_add_connected_lines(line.fbus)
                else:
                    add_bus(line.tbus)
                    try_to_add_connected_lines(line.tbus)

    def add_bus(bus):
        if bus not in used_buses.union(sub_system.buses):
            sub_system.buses.add(bus)
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
