from stinetwork.network.components import Bus, Line, Battery, Disconnector, Production, CircuitBreaker

class Microgrid:
    """ Class defining a microgrid network type """
    def __init__(self, num:int, coordinate:list, connected:bool):
        """ Initializing microgrid network type content 
            Content:
                num(int): microgrid number
                coordinate(list): Position of microgrid
                name(str): microgrid name
        """
        self.num = num
        self.coordinate = coordinate
        self.name = "microgrid" + str(num)
        self.connected = connected

    def add_production(self, production:Production):
        """ Adding production to microgrid network
            Input: production(Production) """
        pass

    def add_battery(self, battery:Battery):
        """ Adding battery to microgrid network
            Input: battery(Battery) """
        pass

    def connect(self):
        self.connected = True

    def disconnect(self):
        self.connected = False


class Distribution:
    """ Class defining a distribution network type """

    def __init__(self):
        """ Initializing distribution network type content 
            Content:
                buses(list): List of buses
                lines(list): List of lines
        """
        self.buses = list()
        self.lines = list()

    def add_buses(self,buses:list):
        """ Adding buses to distribution network
            Input: buses(list(Bus)) """
        self.buses += buses

    def add_lines(self, lines:list):
        """ Adding lines to distribution network
            Input: lines(list(Line)) """
        self.lines = lines

    def add_microgrids(self, microgrids:list):
        """ Adding microgrids to distribution network
            Input: microgrids(list(Microgrid)) """
        self.buses += microgrids

    def update_buses(self):
        self.buses = [bus for bus in self.buses if bus.activated] # Will only include activated buses

    def update_lines(self):
        self.lines = [line for line in self.lines if line.connected] # Will only include connected lines

    def update_microgrids(self):
        self.microgrids = [microgrid for microgrid in self.microgrids if microgrid.connected] # Will only include connected microgrids



if __name__=="__main__":
    pass
