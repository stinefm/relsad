from stinetwork.utils import unique
from .Component import *
from .Line import *
from .Circuitbreaker import *
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

class Disconnector(Component):

    """
    Common base class for disconnectors

    ...

        Attributes
        ----------
        name : string
            Name of the disconnector
        is_open : bool
            Tells if the switch is open (True) or closed (False)
        failed : bool
            True if the disconnector is in a failed state, False if not
        fail_rate : float 
            The failure rate of the disconnector [no of fails per year]
        outage_time : float
            The outage time of the diconnector [hours]
        line : Line
            The line the disconnecor is connected to
        base_bus : Bus 
            Wich bus the disconnector is closes to (for setting coordinates)
        

        Functions 
        ----------
        close(hour) :    

    """

    ## Visual attributes
    color="black"
    edgecolor="black"
    marker="o"
    size=2**2
    handle = mlines.Line2D([], [], marker = marker, markeredgewidth=3, \
                            markersize=size, linestyle = 'None', \
                            color = color, markeredgecolor=edgecolor)
    
    ## Random instance
    ps_random = None

    def __init__(self, name:str, line:Line, bus:Bus, \
                circuitbreaker:CircuitBreaker=None, is_open:bool=False, \
                fail_rate:float=0.014, outage_time:float=1):
        self.name = name
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.prev_open_hour = 0
        self.line = line
        self.circuitbreaker = circuitbreaker

        ## Set coordinate
        self.base_bus = bus
        dx = line.tbus.coordinate[0]-line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1]-line.fbus.coordinate[1]
        if bus==line.tbus:
            dx*=-1
            dy*=-1
        if self.circuitbreaker == None:
            line.disconnectors.append(self)
            self.coordinate = [ \
                self.base_bus.coordinate[0] + dx/4, self.base_bus.coordinate[1] + dy/4]
        else:
            self.circuitbreaker.disconnectors.append(self)
            #line.disconnectors.append(self)
            self.coordinate = [ \
                circuitbreaker.coordinate[0] - dx/10, circuitbreaker.coordinate[1] - dy/10]

        ## History
        self.history = {"is_open":dict()}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Disconnector(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def close(self, hour):
        if hour > self.prev_open_hour or self.line.is_backup:
            self.is_open = False
            self.color = "black"
            if not self.line.connected:
                self.line.connect()
    
    def open(self, hour):
        self.is_open = True
        self.prev_open_hour = hour
        self.color = "white"
        if self.line.connected:
            self.line.disconnect()

    def fail(self, hour):
        self.failed = True
        self.open(hour)

    def not_fail(self, hour):
        self.failed = False
        self.close(hour)

    def update_fail_status(self, hour):
        pass

    def update_history(self, hour):
        self.history["is_open"][hour] = self.is_open

    def get_history(self, attribute:str):
        return self.history[attribute]

    def add_random_seed(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

    def print_status(self):
        pass

if __name__=="__main__":
    pass
