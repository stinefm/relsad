from stinetwork.network.components import Bus, Line, Battery, Disconnector, Production, CircuitBreaker
from stinetwork.topology.paths import find_backup_lines_between_sub_systems

class PowerSystem:

    ## Visual attributes
    color="black"

    def __init__(self):
        """ Initializing power system content 
            Content:
                buses(list): List of buses
                lines(list): List of lines
                comp_dict(dict): Dictionary of components
        """
        self.sub_systems = list()

        self.all_buses = list()
        self.all_lines = list()

        self.active_buses = list()
        self.comp_dict = dict()
        self.active_lines = list()
        self.backup_lines = list()
        self.dist_network_list = list()
        self.microgrid_network_list = list()

    ## Singleton definitions
    __instance = None
    def __new__(cls):
        if PowerSystem.__instance is None:
            PowerSystem.__instance = object.__new__(cls)
        return PowerSystem.__instance

    def add_buses(self,buses:list):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
        self.active_buses += buses
        self.all_buses += buses

    def add_lines(self, lines:list):
        """ Adding lines to power system
            Input: lines(list(Line)) """
        for line in lines:
            if line.is_backup:
                self.backup_lines.append(line)
            self.comp_dict[line.name] = line
            for discon in line.disconnectors:
                self.comp_dict[discon.name] = discon
            if line.circuitbreaker != None:
                cb = line.circuitbreaker
                self.comp_dict[cb.name] = cb
                for discon in cb.disconnectors:
                    self.comp_dict[discon.name] = discon
        self.active_lines += lines
        self.all_lines += lines

    def update(self):
        self.active_buses = [bus for bus in self.all_buses if not bus.trafo_failed] # Will only include not failes buses
        self.active_lines = [line for line in self.all_lines if line.connected] # Will only include connected lines
        for dist_network in self.dist_network_list:
            dist_network.update()
        for microgrid_network in self.microgrid_network_list:
            microgrid_network.update()

    def get_comp(self, name:str):
        try:
            return self.comp_dict[name]
        except BaseException:
            print("Component is not part of the network")

    def get_comp_list(self):
        return self.all_buses+self.all_lines

    def add_distribution_network(self, dist_network):
        self.dist_network_list.append(dist_network)

    def add_microgrid_network(self, microgrid_network):
        self.microgrid_network_list.append(microgrid_network)

    def find_sub_systems(self):

        self.sub_systems = list()
        possible_buses = [bus for bus in self.all_buses]# if bus.toline != None or bus.fromline != None]
        used_buses = list()
        used_lines = list()
        sub_lines = list()
        sub_buses = list()
        sub_system = {"buses":sub_buses,"lines":sub_lines}

        def add_bus(bus):
            if bus not in used_buses+sub_system["buses"]:
                sub_system["buses"].append(bus)
                used_buses.append(bus)

        def try_to_add_connected_lines(bus):
            for line in bus.connected_lines:
                if line in self.active_lines and \
                    line not in used_lines+sub_system["lines"] and \
                    line.connected:
                    sub_system["lines"].append(line)
                    used_lines.append(line)

        while not len(used_buses+used_lines)==len(possible_buses+self.active_lines):
            for _i in range(2):
                for bus in possible_buses:
                    if bus not in used_buses+sub_system["buses"]:
                        if len(sub_system["buses"]+sub_system["lines"]) == 0:
                            add_bus(bus)
                            try_to_add_connected_lines(bus)
                        if bus in sub_system["buses"]:
                            try_to_add_connected_lines(bus)
                        else:
                            for line in sub_system["lines"]:
                                if bus in [line.fbus,line.tbus] or line in bus.connected_lines:
                                    add_bus(bus)
                                    try_to_add_connected_lines(bus)
            
            if sub_system != {"buses":[],"lines":[],"slack":None}:
                self.sub_systems.append(sub_system)
                sub_lines = list()
                sub_buses = list()
                sub_system = {"buses":sub_buses,"lines":sub_lines,"slack":None}
            else:
                break
        if len(self.sub_systems) > 1:
            self.update_backup_lines_between_sub_systems()


    def update_backup_lines_between_sub_systems(self):
        update = False
        for s1 in self.sub_systems:
            for s2 in self.sub_systems:
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
            self.update()
            self.find_sub_systems()
            

    def update_sub_system_slack(self):
        for sub_system in self.sub_systems:
            sub_system["slack"] = None
            for bus in sub_system["buses"]:
                bus.is_slack = False
            self.set_slack(sub_system)
        for sub_system in self.sub_systems:
            if sub_system["slack"] == None:
                self.sub_systems.remove(sub_system)

    def set_slack(self, sub_system):
        ## Distribution network slack buses in sub_system
        for bus in sub_system["buses"]:
            for dist_network in self.dist_network_list:
                if bus == dist_network.get_slack_bus():
                    bus.set_slack()
                    sub_system["slack"] = bus
        ## Buses with battery
        if sub_system["slack"] == None:
            for bus in sub_system["buses"]:
                if bus.battery != None:
                    bus.set_slack()
                    sub_system["slack"] = bus
        ## Buses with production
        if sub_system["slack"] == None:
            for bus in sub_system["buses"]:
                if bus.prod != None:
                    bus.set_slack()
                    sub_system["slack"] = bus
        ## Delete if no possible slack
        if sub_system["slack"] == None:
            self.sub_systems.remove(sub_system)

    def reset_slack_bus(self):
        for dist_network in self.dist_network_list:
            dist_network.reset_slack_bus()
        for microgrid in self.microgrid_network_list:
            microgrid.reset_slack_bus()

    def print_status(self):
        print("Buses:")
        for bus in self.all_buses:
            print("name: {}, trafo_failed={}, pload={:.2f}, is_slack={}, toline={}, fromline={}"\
                    .format(bus.name, bus.trafo_failed, bus.pload, bus.is_slack, bus.toline if bus.toline==None else bus.toline.name, bus.fromline if bus.fromline == None else bus.fromline.name ))
        print("Lines:")
        for line in self.all_lines:
            print("name: {}, failed={}, connected={}".format(line.name, line.failed, line.connected))

class Distribution:
    """ Class defining a distribution network type """

    ## Visual attributes
    color="steelblue"

    def __init__(self, powerSystem:PowerSystem):
        """ Initializing distributed network type content 
            Content:
                buses(list): List of buses
                lines(list): List of lines
                comp_dict(dict): Dictionary of components
                connected_line(Line): Line connected to distrubution network
        """
        self.all_buses = list()
        self.all_lines = list()
        self.active_buses = list()
        self.comp_dict = dict()
        self.active_lines = list()
        self.powerSystem = powerSystem
        self.slack_bus = None

    def add_buses(self,buses:list):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
            bus.handle.color = self.color
            bus.color = self.color
            if bus.is_slack:
                if self.slack_bus == None:
                    self.slack_bus = bus
                else:
                    raise Exception("The distribution network can only have one slack bus")
        self.active_buses += buses
        self.all_buses += buses
        self.powerSystem.add_buses(buses)

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
        self.active_lines += lines
        self.all_lines += lines
        self.powerSystem.add_lines(lines)

    def update(self):
        self.active_buses = [bus for bus in self.all_buses if not bus.trafo_failed] # Will only include not failes buses
        self.active_lines = [line for line in self.all_lines if line.connected] # Will only include connected lines

    def get_slack_bus(self):
        return self.slack_bus

    def reset_slack_bus(self):
        for bus in self.all_buses:
            if bus == self.slack_bus:
                bus.set_slack()
            else:
                bus.is_slack = False


class Microgrid:
    """ Class defining a microgrid network type """

    ## Visual attributes
    color="seagreen"

    def __init__(self, distibutionNetwork:Distribution, connected_line:Line):
        """ Initializing microgrid network type content 
            Content:
                buses(list): List of buses
                lines(list): List of lines
                comp_dict(dict): Dictionary of components
                connected_line(Line): Line connected to distrubution network
        """
        self.all_buses = list()
        self.all_lines = list()
        self.active_buses = list()
        self.comp_dict = dict()
        self.active_lines = list()
        self.distibutionNetwork = distibutionNetwork
        self.connected_line = connected_line
        self.add_lines([connected_line])

    def add_buses(self,buses:list):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
            bus.handle.color = self.color
            bus.color = self.color
        self.active_buses += buses
        self.all_buses += buses
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
        self.active_lines += lines
        self.all_lines += lines
        self.distibutionNetwork.powerSystem.add_lines(lines)

    def update(self):
        self.active_buses = [bus for bus in self.all_buses if not bus.trafo_failed] # Will only include not failes buses
        self.active_lines = [line for line in self.all_lines if line.connected] # Will only include connected lines

    def connect(self):
        self.connected_line.connect()

    def disconnect(self):
        self.connected_line.disconnect()

    def reset_slack_bus(self):
        for bus in self.all_buses:
            bus.is_slack = False

if __name__=="__main__":
    pass
