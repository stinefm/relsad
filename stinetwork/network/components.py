
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


class SlackBus:

    def __init__(self, num:int, coordinate:list, \
                capacity:float):
        self.num = num
        self.name = 'Bus' + str(num)
        self.coordinate = coordinate

        self.voang = 0.0
        self.vomag = 1.0
        self.capacity = capacity
        
        self.toline = 0
        self.fromline = 0
        self.tolinelist = []
        self.nextbus = []
        Bus.busCount += 1


class Bus:
    'Common base class for all distribution buses'
    busCount = 0

    def __init__(self, num, pload=0.0, qload=0.0, coordinate:list=[0,0], \
                ZIP=[0.0, 0.0 ,1.0], vset=0.0, iloss=0, pqcostRatio=100):
        self.num = num
        self.coordinate = coordinate
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
        self.name = 'Bus' + str(num)
        self.toline = 0
        self.fromline = 0
        self.tolinelist = []
        self.nextbus = []
        Bus.busCount += 1

    def add_production(self, production:Production):
        pass

    def add_battery(self, battery:Battery):
        pass


class LoadBreaker:
    
    def __init__(self, num:int, is_open:bool, fail_rate:float, \
                outage_time:float):
        self.num = num
        self.name = "L-breaker" + str(num)
        self.is_open = is_open
        self.fail_rate = fail_rate
        self.outage_time = outage_time


class CircuitBreaker:
    
    def __init__(self, num:int, is_open:bool, fail_rate:float, \
                outage_time:float):
        self.num = num
        self.name = "L-breaker" + str(num)
        self.is_open = is_open
        self.fail_rate = fail_rate
        self.outage_time = outage_time


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
    ibstat : bool
        Line state

    Methods
    -------
    add_load_breaker(load_breaker:LoadBreaker)
        Adds load breaker
    '''
    lineCount = 0

    def __init__(self, fbus:Bus, tbus:Bus, r:float, \
                x:float, length:float=1, fail_rate:float=1, \
                outage_time:float=1, capacity:float=1, ibstat=True):
        self.fbus = fbus
        self.tbus = tbus
        self.r = r
        self.x = x
        self.length = length
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.capacity = capacity
        self.ibstat = ibstat
        self.ploss = 0.0
        self.qloss = 0.0
        Line.lineCount += 1

    def add_load_breaker(self, load_breaker:LoadBreaker):
        pass

if __name__=="__main__":
    pass