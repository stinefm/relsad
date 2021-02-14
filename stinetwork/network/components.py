import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

class Bus:
    ''' 
    Common base class for all distribution buses

    ...

        Attributes
        ----------
        name : string
            Name of the bus
        coordinate : list
            Coordinate of the bus
        pload : float
            The active load at the bus [MW]
        qload : float
            The reactive load at the bus [MVar]
        ZIP : list
        vset : float
        iloss : float
        pqcostRatio : 
        comp : 
        ploadds : float
        qloadds : float
        pblossds : float
        qblossds : float
        dPdV : float
        dQdV : float
        dVdP : float
        dVdQ : float
        dPlossdP : float
        dPlossdQ : float
        dQlossdP : float
        dQlossdQ : float
        dP2lossdP2 : float
        dP2lossdQ2 : float
        lossRatioP :
        lossRatioQ :
        voang : float
        vomag : float 

    '''
    
    busCount = 0

    ## Visual attributes
    marker="o"
    size=5**2
    handle = mlines.Line2D([], [], marker = marker, markeredgewidth=3, \
                            markersize=size, linestyle = 'None')

    def __init__(self, name:str, coordinate:list=[0,0], \
                ZIP=[0.0, 0.0 ,1.0], vset=0.0, iloss=0, pqcostRatio=100, \
                is_slack:bool=False, fail_rate_per_year:float=0.5, \
                outage_time:float=4):
        ## Informative attributes
        self.name = name
        self.coordinate = coordinate

        ## Power flow attributes
        self.pload = 0
        self.qload = 0
        self.pprod = 0
        self.qprod = 0
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
        self.num = Bus.busCount
        self.is_slack = is_slack
        self.toline = None
        self.fromline = None
        self.tolineset = set()
        self.fromlineset = set()
        self.nextbus = set()
        self.connected_lines = set()
        Bus.busCount += 1

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_per_year # failures per year
        self.fail_rate_per_hour = self.fail_rate_per_year/(365*24)
        self.outage_time = outage_time # hours
        self.cost = 0 # cost

        ## Status attribute
        self.trafo_failed = False
        self.remaining_outage_time = 0
        
        ## Production and battery
        self.prod = None
        self.battery = None

        ## History
        self.history = {"pload":list(), "qload":list(), "pprod":list(), "qprod":list()}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Bus(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def reset_load_and_prod_attributes(self):
        self.pload = 0
        self.qload = 0
        self.pprod = 0
        self.qprod = 0

    def set_load(self, load_dict:dict):
        self.pload = 0
        self.qload = 0
        cost_functions = {"Jordbruk":{"A":21.4-17.5,"B":17.5},\
                        "Industri":{"A":132.6-92.5,"B":92.5},\
                        "Handel og tjenester":{"A":220.3-102.4,"B":102.4},\
                        "Offentlig virksomhet":{"A":194.5-31.4,"B":31.4},\
                        "Husholdning":{"A":8.8,"B":14.7}}
        for load_type in load_dict:
            try:
                type_cost = cost_functions[load_type]
                A = type_cost["A"]
                B = type_cost["B"]
                self.set_cost(A+B*1)
                self.pload += load_dict[load_type]["pload"]
                self.qload += load_dict[load_type]["qload"]
            except:
                raise KeyError("Load type {} is not in cost_functions".format(load_type))

    def trafo_fail(self):
        """ 
        Trafo fails, load and generation is set to zero
        """
        self.trafo_failed = True
        self.remaining_outage_time = self.outage_time-1
        self.set_load(0,0)
        if self.prod != None:
            self.prod.set_prod(0,0)
    
    def trafo_not_fail(self):
        self.trafo_failed = False

    def get_battery(self):
        return self.battery

    def get_production(self):
        return self.prod

    def update_fail_status(self):
        if self.trafo_fail:
            self.remaining_outage_time -= 1
            if self.remaining_outage_time == 0:
                self.trafo_not_fail()
        else:
            p_fail = self.fail_rate_per_hour
            if np.random.choice([True,False],p=[p_fail,1-p_fail]):
                self.trafo_fail()
            else:
                self.trafo_not_fail()

    def set_slack(self):
        self.is_slack = True
    
    def print_status(self):
        print("name: {:3s}, trafo_failed={}, pload={:.4f}, " \
            "is_slack={}, toline={}, fromline={}, tolineset={}, " \
            "fromlineset={}, connected_lines={}, cost={:.4f}"\
            .format(self.name, self.trafo_failed, self.pload, self.is_slack, \
                    self.toline if self.toline==None else self.toline.name, self.fromline if self.fromline == None else self.fromline.name,\
                    self.tolineset, self.fromlineset, self.connected_lines, self.cost))

    def update_history(self):
        self.history["pload"].append(self.pload)
        self.history["qload"].append(self.qload)
        self.history["pprod"].append(self.pprod)
        self.history["qprod"].append(self.qprod)

    def get_history(self, attribute:str):
        return self.history[attribute]

    def set_cost(self, cost:float):
        self.cost = cost
    
    def get_cost(self):
        return self.cost

class Line:
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

    def __init__(self, name:str, fbus:Bus, tbus:Bus, r:float, \
                x:float, length:float=1, fail_rate_density_per_year:float=0.2, \
                outage_time:float=2, capacity:float=100, connected=True):
        ## Informative attributes
        self.name = name

        ## Backup
        self.is_backup = False

        ## Topological attributes
        self.fbus = fbus
        self.tbus = tbus
        fbus.connected_lines.add(self)
        tbus.connected_lines.add(self)
        tbus.toline = self
        tbus.tolineset.add(self)
        fbus.fromline = self
        fbus.fromlineset.add(self)
        fbus.nextbus.add(self.tbus)
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
        self.fail_rate_per_year = fail_rate_density_per_year*length # failures per year
        self.fail_rate_per_hour = self.fail_rate_per_year/(365*24)
        self.outage_time = outage_time # hours

        ## Status attribute
        self.connected = connected
        self.failed = False
        self.remaining_outage_time = 0

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
            discon.open()

    def disconnect(self):
        self.connected = False
        self.linestyle="--"
        self.fbus.fromlineset.discard(self)
        if self.fbus.fromline == self:
            if len(self.fbus.fromlineset) > 0:
                self.fbus.fromline = next(iter(self.fbus.fromlineset))
            else:
                self.fbus.fromline = None
        self.tbus.tolineset.discard(self)
        if self.tbus.toline == self:
            if len(self.tbus.tolineset) > 0:
                self.tbus.toline = next(iter(self.tbus.tolineset))
            else:
                self.tbus.toline = None
        self.fbus.nextbus.discard(self.tbus)
        for discon in self.disconnectors:
            if not discon.is_open:
                discon.open()
        if self.circuitbreaker != None:
            if not self.circuitbreaker.is_open:
                self.circuitbreaker.open()

    def connect(self):
        self.connected = True
        self.linestyle="-"
        self.tbus.toline = self
        self.tbus.tolineset.add(self)
        self.fbus.fromline = self
        self.fbus.fromlineset.add(self)
        self.fbus.nextbus.add(self.tbus)
        for discon in self.disconnectors:
            discon.close()
        if self.circuitbreaker != None:
            self.circuitbreaker.close()

    def fail(self):
        self.failed = True
        self.remaining_outage_time = self.outage_time-1
        self.disconnect()

    def not_fail(self):
        self.failed = False
        if not self.is_backup:
            self.connect()

    def change_direction(self):
        self.fbus.fromlineset.discard(self)
        self.tbus.fromlineset.add(self)
        self.tbus.tolineset.discard(self)
        self.fbus.tolineset.add(self)
        if self.fbus.fromline == self:
            self.fbus.fromline = next(iter(self.fbus.fromlineset)) if len(self.fbus.fromlineset)>0 else None
        if self.tbus.toline == self:
            self.tbus.toline = next(iter(self.tbus.tolineset)) if len(self.tbus.tolineset)>0 else None
        self.fbus.toline = self
        self.tbus.fromline = self
        self.fbus.nextbus.discard(self.tbus)
        self.tbus.nextbus.add(self.fbus)
        i_broken = self.tbus.num
        self.tbus.num = self.fbus.num
        self.fbus.num = i_broken
        bus = self.fbus
        self.fbus = self.tbus
        self.tbus = bus        

    def update_fail_status(self):
        if self.is_backup:
            self.disconnect()
        if self.failed:
            self.remaining_outage_time -= 1
            if self.remaining_outage_time == 0:
                self.not_fail()
        else:
            p_fail = self.fail_rate_per_hour
            if np.random.choice([True,False],p=[p_fail,1-p_fail]):
                self.fail()
            else:
                self.not_fail()

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

        Pfrom = g * v1 * v1 - v1 * v2 * tij(g, b, teta1, teta2)
        Pto = g * v2 * v2 - v1 * v2 * tij(g, b, teta2, teta1)
        Qfrom = -(b + bsh) * v1 * v1 - v1 * v2 * uij(g, b, teta1, teta2)
        Qto = -(b + bsh) * v2 * v2 - v1 * v2 * uij(g, b, teta2, teta1)

        return Pfrom,Qfrom,Pto,Qto

    def print_status(self):
        print("name: {:5s}, failed={}, connected={}".format(self.name, self.failed, self.connected))


class CircuitBreaker:

    """
    Common base class for circuit breakers

    ...

        Attributes
        ----------
        name : string
            Name of the circuit breaker
        coordinate : list
            Coordinate of the circuit breaker
        is_open : bool
            Tells if the switch is open (True) or closed (False)
        failed : bool
            True if the circuit breaker is in a failed state, False if not
        fail_rate : float 
            The failure rate of the circuit breaker [no of fails per year]
        outage_time : float
            The outage time of the circuit breaker [hours]
        line : Line
            The line the circuit breaker is connected to
        disconnecter : list(Disconnectors) 
            Which disconnectors that are connected to the circuit breaker
        line.circuitbreaker : 

        Functions 
        ----------
        close() :    

        """

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

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Circuitbreaker(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def close(self):
        self.is_open = False
        self.color = "black"

    def open(self):
        self.is_open = True
        self.color = "white"
        if self.line.connected == True:
            self.line.disconnect()
        for discon in self.disconnectors:
            if not discon.is_open:
                discon.open()

    def fail(self):
        self.failed = True
        self.open()

    def not_fail(self):
        self.failed = False
        self.close()


class Disconnector:

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
        close() :    

    """

    ## Visual attributes
    color="black"
    edgecolor="black"
    marker="o"
    size=2**2
    handle = mlines.Line2D([], [], marker = marker, markeredgewidth=3, \
                            markersize=size, linestyle = 'None', \
                            color = color, markeredgecolor=edgecolor)
    
    def __init__(self, name:str, line:Line, bus:Bus, \
                circuitbreaker:CircuitBreaker=None, is_open:bool=False, \
                fail_rate:float=0.014, outage_time:float=1):
        self.name = name
        self.is_open = is_open
        self.failed = False
        self.fail_rate = fail_rate
        self.outage_time = outage_time
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

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Disconnector(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def close(self):
        self.is_open = False
        self.color = "black"
    
    def open(self):
        self.is_open = True
        self.color = "white"
        if self.line.connected == True:
            self.line.disconnect()

    def fail(self):
        self.failed = True
        self.open()

    def not_fail(self):
        self.failed = False
        self.close()


class Battery:
    """
    Common class for batteries
     
    ...
     
    Attributes
    ----------
    name : string
        Name of the battery
    bus : Bus
        The bus the battery is connected to
    injPmax : float
        The maximum active power that the battery can inject [MW]
    injQmax : float
        The maximum reactive power that the battery can inject [MVar]
    E_max : float
        The maximum capacity of the battery [MWh]
    SOC_min : float
        The minimal state of charge level in the battery 
    SOC_max : float 
        The maximum state of charge level in the battery 
    n_battery : float
        The battery efficiency  
    P_inj : float
        The injected active power in the battery [MW]
    Q_inj : float
        The injected reactive power in the battery [MVar]
    SOC : float
        The state of charge of the battery 
    E_battery : float
        The amount of energy stored in the battery [MWh]
    
    Methods 
    ----------
    update_SOC() 
        Updates the SOC in the battery
    charge(P_ch)
        Charge the battery 
    discharge(P_dis)
        Discharge the battery 
    print_status()
        Prints the status of the battery

    """

    def __init__(self, name:str, bus:Bus, inj_p_max:float=1, inj_q_max:float=1, \
                E_max:float=3, SOC_min:float=0.2, SOC_max:float=1, n_battery:float=0.97):
        
        """
        Constructs all the necessary attributes for the production object

        Parameters
        ----------
        name : string
            Name of the battery
        bus : Bus
            The bus the battery is connected to
        inj_p_max : float
            The maximum active power that the battery can inject [MW]
        inj_q_max : float
            The maximum reactive power that the battery can inject [MVar]
        E_max : float
            The maximum capacity of the battery [MWh]
        SOC_min : float
            The minimal state of charge level in the battery 
        SOC_max : float 
            The maximum state of charge level in the battery 
        n_battery : float
            The battery efficiency  
        P_inj : float
            The injected active power in the battery [MW]
        Q_inj : float
            The injected reactive power in the battery [MVar]
        SOC : float
            The state of charge of the battery 
        E_battery : float
            The amount of energy stored in the battery [MWh]
        
        
        """
        
        self.name = name
        self.bus = bus
        bus.battery = self

        self.inj_p_max = inj_p_max  # MW
        self.inj_q_max = inj_q_max  # MVar
        self.inj_max = self.inj_p_max
        self.f_inj_p = 1 # active capacity fraction
        self.f_inj_q = self.inj_q_max/self.inj_max # reactive capacity fraction

        self.E_max = E_max      # MWh
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.n_battery = n_battery

        self.P_inj = 0.0        # MW
        self.Q_inj = 0.0        # MVar
        self.SOC = SOC_min
        self.E_battery = self.SOC*self.E_max    # MWh
        self.update_SOC()

        ## History
        self.history = {"SOC":list()}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Battery(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def update_SOC(self):
        """
        Updates the SOC in the battery

        Paramters
        ----------
        SOC : float
            The state of charge of the battery
        E_battery : float
            The amount of energy stored in the battery [MWh]
        E_max : float
            The maximum capacity of the battery [MWh]
        
        Returns
        ----------
        None

        """
        self.SOC = self.E_battery/self.E_max

    def charge(self, p_ch):

        """
        Charge the battery 
        
        Decides how much the battery can charge based on the available energy that can be stored, the maximum power that can be injected, and the maximum state of charge of the battery
        
        Updates the state of charge of the battery

        Returns a float telling how much energy the battery is not able to charge
        

        Parameters
        ----------
        p_ch : float
            Amount of available energy in the network for the battery to charge [MW]

        Returns
        ----------
        P_ch_remaining : float
            Amount of wanted active energy from the network exceeding battery capacity [MW]


        """

        p_ch_remaining = 0
        if p_ch > self.inj_p_max:
            p_ch_remaining += p_ch - self.inj_p_max
            if p_ch == np.inf:
                p_ch = self.inj_p_max
            else:
                p_ch -= p_ch_remaining
        dE = self.n_battery*p_ch
        E_tr = self.E_battery + dE
        SOC_tr = E_tr/self.E_max
        dSOC = dE/self.E_max
        if SOC_tr > self.SOC_max:
            f = 1-(SOC_tr-self.SOC_max)/dSOC
            self.E_battery += f*dE
            p_ch_remaining += (1-f)*p_ch
        else:
            self.E_battery += dE
            p_ch_remaining += 0
        self.update_SOC()
        return p_ch_remaining

    def discharge(self, p_dis, q_dis):

        """
        Discharge the battery 
        
        Decides how much the battery can discharge based on the available energy in the battery limited by the state of charge, the maximum power that can be injected, and the wanted amount of energy from the battery
        
        Updates the state of charge of the battery

        Returns a float telling how much energy the battery is not able to discharge
        

        Parameters
        ----------
        p_dis : float
            Amount of wanted active energy from the network [MW]
        q_dis : float
            Amount of wanted reactive energy from the network [MW]

        Returns
        ----------
        p_ch_remaining : float
            Amount of wanted active energy from the network exceeding battery capacity [MW]
        q_ch_remaining : float
            Amount of wanted reactive energy from the network exceeding battery capacity [MW]

        """

        p_dis_remaining = 0
        q_dis_remaining = 0
        if p_dis > self.inj_p_max:
            p_dis_remaining += p_dis - self.inj_p_max
            p_dis -= p_dis_remaining
        if q_dis > self.inj_q_max:
            q_dis_remaining += q_dis - self.inj_q_max
            q_dis -= q_dis_remaining
        if p_dis + q_dis > self.inj_max:
            f_p = p_dis/(p_dis + q_dis) # active fraction
            f_q = 1-f_p # reactive fraction
            diff = p_dis + q_dis - self.inj_max
            p_dis_remaining += diff*(1-f_p)
            q_dis_remaining += diff*(1-f_q)
            p_dis -= diff*(1-f_p)
            q_dis -= diff*(1-f_q)

        dE = 1/self.n_battery*(p_dis + q_dis)
        E_tr = self.E_battery - dE
        SOC_tr = E_tr/self.E_max
        dSOC = dE/self.E_max
        if SOC_tr < self.SOC_min:
            f = 1-(self.SOC_min-SOC_tr)/dSOC
            self.E_battery -= f*dE
            p_dis_remaining += (1-f)*p_dis
            q_dis_remaining += (1-f)*q_dis
        else:
            self.E_battery -= dE
        self.update_SOC()
        return p_dis_remaining, q_dis_remaining

    def print_status(self):

        """
        Prints the status of the battery
        
        Returns
        ----------
        None
        """

        print("Battery status")
        print("name: {}".format(self.name))
        print("parent bus: {}".format(self.bus.name))
        print("inj_p_max: {} MW".format(self.inj_p_max))
        print("inj_q_max: {} MVar".format(self.inj_q_max))
        print("E_max: {} MWh".format(self.E_max))
        print("Efficiency: {} %".format(self.n_battery*100))
        print("SOC_min: {}".format(self.SOC_min))
        print("SOC_max: {}".format(self.SOC_max))
        print("SOC: {:.2f}".format(self.SOC))

    def update_bus_load_and_prod(self, system_load_balance_p:float, system_load_balance_q:float):
        """
         Updates the load and production on the bus based on the system load balance.
         If the balance is negative, there is a surplus of production, and the battery will charge.
         If the balance is positive, there is a shortage of production, and the battery will discharge.
        
        Parameters 
        ----------
            system_load_balance_p : float
                Active system load balance
            system_load_balance_q : float
                Reactive system load balance
        """
        p,q = system_load_balance_p, system_load_balance_q

        pprod,qprod,pload,qload = 0,0,0,0
        if p >= 0 and q >= 0:
            p_dis, q_dis = self.discharge(p,q)
            pprod = p - p_dis
            qprod = q - q_dis
        if p < 0 and q >= 0:
            if -p == np.inf:
                pload = self.inj_p_max - self.charge(self.inj_p_max)
            else:
                pload = -p - self.charge(-p)
            qprod = q - self.discharge(0,q)[1]
        if p >= 0 and q < 0:
            pprod = p - self.discharge(p,0)[0]  
        if p < 0 and q < 0:
            if -p == np.inf:
                pload = self.inj_p_max - self.charge(self.inj_p_max)
            else:
                pload = -p - self.charge(-p)
        self.update_history()
        if self.SOC > self.SOC_min:
            self.bus.pprod += pprod
            self.bus.qprod += qprod
        if self.SOC < self.SOC_max:
            self.bus.pload += pload
            self.bus.qload += qload
        prem = p + pload - pprod
        qrem = q + qload - qprod
        return prem, qrem

    def update_history(self):
        self.history["SOC"].append(self.SOC)

    def get_history(self, attribute:str):
        return self.history[attribute]

class Production:

    """
    Common class for production 
     
    ...
     
    Attributes
    ----------
    name : string
        Name of the production unit
    bus : Bus
        The bus the production unit is connected to
    pprod : float
        The active power produced by the production unit [MW]
    qprod : float
        The reactive power produced by the production unit [MVar]
    pmax : float 
        The maximum active power that can be produced by the production unit [MW]
    qmax : float 
        The maximum reactive power that can be produced by the production unit [MVar]


    Methods 
    ----------
    set_prod(pprod, qprord)
        Decides how much active and reactive power that will be produced 
    update_bus_load()
        Updates the load on the bus with the amount of generated active and reactive power 

    """
    
    def __init__(self, name:str, bus:Bus, pmax:float=1, qmax:float=0):
        
        """
        Constructs all the necessary attributes for the production object
        
        Parameters 
        ----------
            name : string
                Name of the production unit
            bus : Bus
                The bus the production unit is connected to
            pprod : float
                The active power produced by the production unit [MW]
            qprod : float
                The reactive power produced by the production unit [MVar]
            pmax : float 
                The maximum active power that can be produced by the production unit [MW]
            qmax : float 
                The maximum reactive power that can be produced by the production unit [MVar]
        """
        self.name = name
        self.bus = bus
        bus.prod = self
        self.pprod = 0
        self.qprod = 0
        self.pmax = pmax
        self.qmax = qmax

    def __str__(self):
        return self.name

    def __repr__(self):
        return f'Production(name={self.name})'

    def __eq__(self,other):
        try:return self.name == other.name
        except:False

    def __hash__(self):
        return hash(self.name)

    def set_prod(self, pprod:float, qprod:float):

        """
         Decides how much active and reactive power that will be produced
         If the produced power exceeds the maximal limit, the produced power is set to maximum limit
         The function updates the production on the bus by using the function update_bus_load()

         Parameters
         ----------
        pprod : float
            The active power produced by the production unit [MW]
        qprod : float
            The reactive power produced by the production unit [MVar]
        pmax : float 
            The maximum active power that can be produced by the production unit [MW]
        qmax : float 
            The maximum reactive power that can be produced by the production unit [MVar]

         Returns
         ----------
         None

        """
        if pprod > self.pmax:
            self.pprod = self.pmax
        else:
            self.pprod = pprod
        if qprod > self.qmax:
            self.qprod = self.qmax
        else:
            self.qprod = qprod
        self.update_bus_prod()

    def update_bus_prod(self):

        """
         Updates the production on the bus with the amount of generated active and reactive power 
         Sets the active production at the bus equal the active production at the bus minus the generated active power
         Sets the reactive production at the bus equal the reactive production at the bus minus the generated reactive power
        """
        self.bus.pprod = self.pprod
        self.bus.qprod = self.qprod


if __name__=="__main__":
    pass