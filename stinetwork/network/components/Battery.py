from stinetwork.utils import unique
from .Component import *
from .Bus import *
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

class Battery(Component):
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

    ## Random instance
    ps_random = None

    def __init__(self, name:str, bus:Bus, inj_p_max:float=0.5, inj_q_max:float=0.5, \
                E_max:float=1, SOC_min:float=0.2, SOC_max:float=1, n_battery:float=0.97):
        
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
        bus.set_cost(1) ## Add symbolic cost to shedding battery load

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

        self.lock = False

        ## History
        self.history = {"SOC":dict()}

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

        if self.lock:
            return p, q

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
        if self.SOC > self.SOC_min:
            self.bus.pprod += pprod
            self.bus.qprod += qprod
        if self.SOC < self.SOC_max:
            self.bus.pload += pload
            self.bus.qload += qload
        prem = p + pload - pprod
        qrem = q + qload - qprod
        return prem, qrem

    def update_history(self, hour):
        self.history["SOC"][hour] = self.SOC

    def get_history(self, attribute:str):
        return self.history[attribute]

    def update_fail_status(self, hour):
        if self.bus.trafo_failed:
            self.lock = True
        else:
            self.lock = False

    def add_random_seed(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

if __name__=="__main__":
    pass