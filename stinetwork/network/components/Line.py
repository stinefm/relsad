from stinetwork.utils import unique
from .Component import *
from .Bus import *
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

class Line(Component):
    r'''
    A class used to represent an electrical Line

    ...

    Attributes
    ----------
    fbus : Bus
        Sending bus
    tbus : Bus
        Receiving bus
    r : float
        Resistance \[Ohm\]
    x : float
        Reactance \[\]
    length : float
        Length of line \[km\]
    fail_rate : float
        Failure rate \[fault/year/km\]
    outage_time : float
        Outage time \[hours/fault\]
    capacity : float
        Line capacity \[MW\]
    connected : bool
        Line state

    Methods
    -------
    add_load_breaker(load_breaker:LoadBreaker)
        Adds load breaker
    '''
    lineCount = 0

    ## Visual attributes
    linestyle="-"
    handle = mlines.Line2D([], [], linestyle = linestyle)

    ## Random instance
    ps_random = None

    def __init__(self, name:str, fbus:Bus, tbus:Bus, r:float, \
                x:float, length:float=1, fail_rate_density_per_year:float=0.2, \
                outage_time:float=4, capacity:float=100, connected=True):
        ## Informative attributes
        self.name = name

        ## Backup
        self.is_backup = False

        ## Topological attributes
        self.fbus = fbus
        self.tbus = tbus
        fbus.connected_lines.append(self)
        tbus.connected_lines.append(self)
        tbus.toline = self
        tbus.tolinelist.append(self)
        fbus.fromline = self
        fbus.fromlinelist.append(self)
        fbus.nextbus.append(self.tbus)
        self.disconnectors = list()
        self.circuitbreaker = None
        self.parent_network = None
        Line.lineCount += 1

        ##  Power flow attributes
        self.r = r
        self.x = x
        self.length = length
        self.capacity = capacity # MW
        self.ploss = 0.0
        self.qloss = 0.0

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_density_per_year*length # failures per year
        self.fail_rate_per_hour = self.fail_rate_per_year/(365*24)
        self.outage_time = outage_time # hours

        ## Status attribute
        self.connected = connected
        self.failed = False
        self.remaining_outage_time = 0

        ## History
        self.history = {"p_from":dict(), "q_from":dict(), "p_to":dict(), \
                        "q_to":dict(), "remaining_outage_time":dict(), \
                        "failed":dict(), "line_loading":dict()}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Line(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def set_backup(self):
        self.is_backup = True
        for discon in self.disconnectors:
            discon.open(hour=1)

    def disconnect(self):
        self.connected = False
        self.linestyle="--"
        self.fbus.fromlinelist.remove(self)
        if self.fbus.fromline == self:
            if len(self.fbus.fromlinelist) > 0:
                self.fbus.fromline = next(iter(self.fbus.fromlinelist))
            else:
                self.fbus.fromline = None
        self.tbus.tolinelist.remove(self)
        if self.tbus.toline == self:
            if len(self.tbus.tolinelist) > 0:
                self.tbus.toline = next(iter(self.tbus.tolinelist))
            else:
                self.tbus.toline = None
        self.fbus.nextbus.remove(self.tbus)

    def connect(self):
        self.connected = True
        self.linestyle="-"
        self.tbus.toline = self
        self.tbus.tolinelist.append(self)
        self.fbus.fromline = self
        self.fbus.fromlinelist.append(self)
        self.fbus.nextbus.append(self.tbus)
        
    def fail(self, hour):
        self.failed = True
        self.remaining_outage_time = self.outage_time
        if self.connected:
            for discon in self.disconnectors:
                if not discon.is_open:
                    discon.open(hour)
            self.parent_network.connected_line.circuitbreaker.open(hour)
            if self.parent_network.child_network_list is not None:
                for child_network in self.parent_network.child_network_list:
                    child_network.connected_line.circuitbreaker.open(hour)

    def not_fail(self, hour):
        self.failed = False
        if not self.is_backup:
            for discon in self.disconnectors:
                if discon.is_open:
                    discon.close(hour)
            if self == self.parent_network.connected_line:
                self.circuitbreaker.close(hour)

    def change_direction(self):
        self.fbus.fromlinelist.remove(self)
        self.tbus.fromlinelist.append(self)
        self.tbus.tolinelist.remove(self)
        self.fbus.tolinelist.append(self)
        if self.fbus.fromline == self:
            self.fbus.fromline = next(iter(self.fbus.fromlinelist)) if len(self.fbus.fromlinelist)>0 else None
        if self.tbus.toline == self:
            self.tbus.toline = next(iter(self.tbus.tolinelist)) if len(self.tbus.tolinelist)>0 else None
        self.fbus.toline = self
        self.tbus.fromline = self
        self.fbus.nextbus.remove(self.tbus)
        self.tbus.nextbus.append(self.fbus)
        i_broken = self.tbus.num
        self.tbus.num = self.fbus.num
        self.fbus.num = i_broken
        bus = self.fbus
        self.fbus = self.tbus
        self.tbus = bus        

    def update_fail_status(self, hour):
        if self.is_backup:
            for discon in self.disconnectors:
                if not discon.is_open:
                    discon.open(hour)
        if self.failed:
            self.remaining_outage_time -= 1
            if self.remaining_outage_time == 0:
                self.not_fail(hour)
        else:
            p_fail = self.fail_rate_per_hour
            if self.ps_random.choice([True,False],p=[p_fail,1-p_fail]):
                self.fail(hour)
            else:
                self.not_fail(hour)

    def get_line_load(self):
        """ Get the flow on the line
        """

        def uij(gij,bij,tetai,tetaj):
            return (gij*np.sin(tetai-tetaj)-bij*np.cos(tetai-tetaj))

        def tij(gij,bij,tetai,tetaj):
            return (gij*np.cos(tetai-tetaj)+bij*np.sin(tetai-tetaj))

        def bij(R, X):
            return (1.0 / complex(R, X)).imag

        def gij(R, X):
            return (1.0 / complex(R, X)).real

        fbus = self.fbus
        tbus = self.tbus
        bsh = 0.0           # No shunts included so far
        teta1 = fbus.voang
        teta2 = tbus.voang
        v1 = fbus.vomag
        v2 = tbus.vomag
        b = bij(self.r,self.x)
        g = gij(self.r,self.x)

        p_from = g * v1 * v1 - v1 * v2 * tij(g, b, teta1, teta2)
        p_to = g * v2 * v2 - v1 * v2 * tij(g, b, teta2, teta1)
        q_from = -(b + bsh) * v1 * v1 - v1 * v2 * uij(g, b, teta1, teta2)
        q_to = -(b + bsh) * v2 * v2 - v1 * v2 * uij(g, b, teta2, teta1)

        return p_from,q_from,p_to,q_to

    def get_line_loading(self):
        """ Get the loading on the line in percent
        """
        p_from = self.get_line_load()[0]
        return abs(p_from)/self.capacity*100

    def print_status(self):
        print("name: {:5s}, failed={}, connected={}".format(self.name, self.failed, self.connected))

    def get_disconnectors(self):
        return self.disconnectors

    def add_parent_network(self, network):
        """
        Adds parent network
        """
        self.parent_network = network

    def update_history(self, hour):
        p_from,q_from,p_to,q_to = self.get_line_load()
        self.history["p_from"][hour] = p_from
        self.history["q_from"][hour] = q_from
        self.history["p_to"][hour] = p_to
        self.history["q_to"][hour] = q_to
        self.history["remaining_outage_time"][hour] = self.remaining_outage_time
        self.history["failed"][hour] = self.failed
        self.history["line_loading"][hour] = self.get_line_loading()

    def get_history(self, attribute:str):
        return self.history[attribute]

    def add_random_seed(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

if __name__=="__main__":
    pass
