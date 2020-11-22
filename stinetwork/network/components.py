import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np


class Battery:
    'Common class for Batteries'
    batteryCount = 0
    def __init__(self, svcstat = 1, vref=0.0, injPmax = 0.0, injPmin = 0.0, injQmax = 0.0, injQmin = 0.0, slopeP = 0.0, slopeQ = 0.0 ):
        self.stat = svcstat
        self.vref = vref
        self.injPmax = injPmax
        self.injPmin = injPmin
        self.injQmax = injQmax
        self.injQmin = injQmin
        self.Pinj = 0.0
        self.Qinj = 0.0
        self.Estorage = 0.0
        self.slopeP = slopeP
        self.slopeQ = slopeQ
        Battery.batteryCount += 1


class Production:
    
    def __init__(self, pprod:float, qprod:float, \
                pmax:float, qmax:float):
        self.pprod = pprod
        self.qprod = qprod
        self.pmax = pmax
        self.qmax = qmax


class Bus:
    'Common base class for all distribution buses'
    busCount = 0

    ## Visual attributes
    color="steelblue"
    marker="o"
    size=5**2
    handle = mlines.Line2D([], [], marker = marker, markeredgewidth=3, \
                            markersize=size, linestyle = 'None', \
                            color = color)

    def __init__(self, num, pload=0.0, qload=0.0, coordinate:list=[0,0], \
                ZIP=[0.0, 0.0 ,1.0], vset=0.0, iloss=0, pqcostRatio=100):
        ## Informative attributes
        self.num = num
        self.name = 'B' + str(num)
        self.coordinate = coordinate
        Bus.busCount += 1

        ## Power flow attributes
        self.pload = pload
        self.qload = qload
        self.ZIP = ZIP
        self.vset = vset
        self.iloss = iloss
        self.pqcostRatio = pqcostRatio
        self.comp = 0
        self.ploadds = 0.0      # Active accumulated load at node
        self.qloadds = 0.0      # Reactive accumulated load at node
        self.pblossds = 0.0     # Active accumulated line loss at node
        self.qblossds = 0.0     # Active accumulated line loss at node
        self.dPdV = 0.0
        self.dQdV = 0.0
        self.dVdP = 0.0
        self.dVdQ = 0.0
        self.dPlossdP = 0.0
        self.dPlossdQ = 0.0
        self.dQlossdP = 0.0
        self.dQlossdQ = 0.0
        self.dP2lossdP2 = 1.0   # To be able to run the voltage optimization also in the first iteration
        self.dP2lossdQ2 = 1.0   # To be able to run the voltage optimization also in the first iteration
        self.lossRatioP = 0.0
        self.lossRatioQ = 0.0
        self.voang = 0.0
        self.vomag = 1.0

        ## Topological attributes
        self.toline = 0
        self.fromline = 0
        self.tolinelist = []
        self.nextbus = []
        self.connected_lines = list()

        ## Status attribute
        self.failed = False

    def add_production(self, production:Production):
        pass

    def add_battery(self, battery:Battery):
        pass

    def fail(self):
        self.failed = True
        for line in self.connected_lines:
            if len(line.disconnectors)==0:
                line.circuitbreaker.open()
            elif len(line.disconnectors)==1:
                line.disconnectors[0].open()
            else:
                for discon in line.disconnectors:
                    if discon.base_bus == self:
                        discon.open()
    
    def not_fail(self):
        self.failed = False


class Line:
    '''
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
    color="steelblue"
    linestyle="-"
    handle = mlines.Line2D([], [], linestyle = linestyle, \
                            color = color)

    def __init__(self, num:int, fbus:Bus, tbus:Bus, r:float, \
                x:float, length:float=1, fail_rate_density:float=1, \
                outage_time:float=1, capacity:float=1, connected=True):
        ## Informative attributes
        self.num = num
        self.name = 'L' + str(num)

        ## Topological attributes
        self.fbus = fbus
        self.tbus = tbus
        fbus.connected_lines.append(self)
        tbus.connected_lines.append(self)
        self.disconnectors = list()
        self.circuitbreaker = None
        Line.lineCount += 1

        ##  Power flow attributes
        self.r = r
        self.x = x
        self.length = length
        self.capacity = capacity
        self.ploss = 0.0
        self.qloss = 0.0

        ## Reliabilility attributes
        self.fail_rate = fail_rate_density*length
        self.outage_time = outage_time

        ## Status attribute
        self.connected = connected
        self.failes = False

    def disconnect(self):
        self.connected = False
        self.linestyle="--"

    def connect(self):
        self.connected = True
        self.linestyle="-"

    def fail(self):
        self.disconnect()
        if len(self.disconnectors) == 1:
            iso_bus = self.disconnectors[0].base_bus
            self.disconnectors[0].open()
            if self.tbus == iso_bus:
                self.fbus.fail()
            else:
                self.tbus.fail()
        elif len(self.disconnectors) == 2:
            for discon in self.disconnectors:
                discon.open()

        if self.circuitbreaker != None:
            self.circuitbreaker.open()

    def not_fail(self):
        self.connect()

class CircuitBreaker:

    ## Visual attributes
    color="black"
    edgecolor="black"
    marker="s"
    size=3**2
    handle = mlines.Line2D([], [], marker = marker, markeredgewidth=3, \
                            markersize=size, linestyle = 'None', \
                            color = color, markeredgecolor=edgecolor)
    
    def __init__(self, name:str, line:Line, is_open:bool=False, section_time:float=1, \
                fail_rate:float=0.014, outage_time:float=1):
        self.name = name

        dx = line.tbus.coordinate[0]-line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1]-line.fbus.coordinate[1]
        self.coordinate = [ \
            line.fbus.coordinate[0] + dx/3, line.fbus.coordinate[1] + dy/3]
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.line = line
        self.disconnectors = list()
        self.line.circuitbreaker = self
        if is_open:
            self.line.disconnect()
        else:
            self.line.connect()

    def close(self):
        self.is_open = False
        self.color = "black"
        self.line.connect()

    def open(self):
        self.is_open = True
        self.color = "white"
        self.line.disconnect()
        for discon in self.disconnectors:
            discon.open()

    def fail(self):
        self.failed = True
        self.open()

    def not_fail(self):
        self.failed = False
        self.close()

class Disconnector:

    ## Visual attributes
    color="black"
    edgecolor="black"
    marker="o"
    size=2**2
    handle = mlines.Line2D([], [], marker = marker, markeredgewidth=3, \
                            markersize=size, linestyle = 'None', \
                            color = color, markeredgecolor=edgecolor)
    
    def __init__(self, name:str, line:Line, bus:Bus, \
                circuit_br:CircuitBreaker=None, is_open:bool=False, \
                fail_rate:float=0.014, outage_time:float=1):
        self.name = name
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.line = line

        ## Set coordinate
        self.base_bus = bus
        dx = line.tbus.coordinate[0]-line.fbus.coordinate[0]
        dy = line.tbus.coordinate[1]-line.fbus.coordinate[1]
        if bus==line.tbus:
            dx*=-1
            dy*=-1
        if circuit_br == None:
            line.disconnectors.append(self)
            self.coordinate = [ \
                self.base_bus.coordinate[0] + dx/4, self.base_bus.coordinate[1] + dy/4]
        else:
            circuit_br.disconnectors.append(self)
            #line.disconnectors.append(self)
            self.coordinate = [ \
                circuit_br.coordinate[0] - dx/10, circuit_br.coordinate[1] - dy/10]

        ## Connect/Disconnect line based on status
        if is_open:
            self.line.disconnect()
        else:
            self.line.connect()

    def close(self):
        self.is_open = False
        self.color = "black"
        self.line.connect()
    
    def open(self):
        self.is_open = True
        self.color = "white"
        self.line.disconnect()

    def fail(self):
        self.failed = True
        self.open()

    def not_fail(self):
        self.failed = False
        self.close()


if __name__=="__main__":
    pass