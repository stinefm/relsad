from stinetwork.network.components import Bus, Line, Battery, Disconnector, Production, CircuitBreaker

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
        self.active_buses = [bus for bus in self.all_buses if not bus.failed] # Will only include not failes buses
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

    def add_distribution_network(self, dist_network):
        self.dist_network_list.append(dist_network)

    def add_microgrid_network(self, microgrid_network):
        self.microgrid_network_list.append(microgrid_network)

    def find_sub_systems(self):
        self.sub_systems = list()
        used_buses = list()
        used_lines = list()
        sub_lines = list()
        sub_buses = list()
        sub_system = {"buses":sub_buses,"lines":sub_lines}
        while not len(used_buses+used_lines)==len(self.active_buses+self.active_lines):
            for bus in self.active_buses:
                if bus not in used_buses+sub_system["buses"]:
                    if len(sub_system["buses"]+sub_system["lines"]) == 0:
                        sub_system["buses"].append(bus)
                        used_buses.append(bus)
                    if bus in sub_system["buses"]:
                        for con_line in bus.connected_lines:
                            if con_line in self.active_lines and con_line not in used_lines+sub_system["lines"]:
                                sub_system["lines"].append(con_line)
                                used_lines.append(con_line)
                    else:
                        for line in sub_system["lines"]:
                            if bus in [line.fbus,line.tbus] and bus not in used_buses+sub_system["buses"]:
                                sub_system["buses"].append(bus)
                                used_buses.append(bus)
                                for con_line in bus.connected_lines:
                                    if con_line in self.active_lines and con_line not in used_lines+sub_system["lines"]:
                                        sub_system["lines"].append(con_line)
                                        used_lines.append(con_line)

            self.sub_systems.append(sub_system)
            sub_lines = list()
            sub_buses = list()
            sub_system = {"buses":sub_buses,"lines":sub_lines}

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

    def add_buses(self,buses:list):
        """ Adding buses to power system
            Input: buses(list(Bus)) """
        for bus in buses:
            self.comp_dict[bus.name] = bus
            bus.handle.color = self.color
            bus.color = self.color
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
        self.active_buses = [bus for bus in self.all_buses if not bus.failed] # Will only include not failes buses
        self.active_lines = [line for line in self.all_lines if line.connected] # Will only include connected lines

class Microgrid:
    """ Class defining a microgrid network type """

    ## Visual attributes
    color="seagreen"

    def __init__(self, powerSystem:PowerSystem, connected_line:Line):
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
        self.powerSystem = powerSystem
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
        self.active_buses = [bus for bus in self.all_buses if not bus.failed] # Will only include not failes buses
        self.active_lines = [line for line in self.all_lines if line.connected] # Will only include connected lines

    def connect(self):
        self.connected_line.connect()

    def disconnect(self):
        self.connected_line.disconnect()

if __name__=="__main__":
    pass
