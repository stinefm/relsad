from stinetwork.network.components import Bus, Line, Battery, LoadBreaker, Production, SlackBus, CircuitBreaker

class Microgrid:
    """ Class defining a microgrid network type """
    def __init__(self, num:int, coordinate:list):
        """ Initializing microgrid network type content 
            Content:
                num(int): microgrid number
                coordinate(list): Position of microgrid
                name(str): microgrid name
        """
        self.num = num
        self.coordinate = coordinate
        self.name = "microgrid" + str(num)

    def add_production(self, production:Production):
        """ Adding production to microgrid network
            Input: production(Production) """
        pass

    def add_battery(self, battery:Battery):
        """ Adding battery to microgrid network
            Input: battery(Battery) """
        pass


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
        self.lines += lines

    def add_microgrids(self, microgrids:list):
        """ Adding microgrids to distribution network
            Input: microgrids(list(Microgrid)) """
        self.buses += microgrids



if __name__=="__main__":
    pass
