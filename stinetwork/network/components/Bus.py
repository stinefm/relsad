from stinetwork.utils import unique
from .Component import *
import matplotlib.patches as mpatches
import matplotlib.lines as mlines
import numpy as np

class Bus(Component):
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

    ## Random instance
    ps_random = None

    def __init__(self, name:str, coordinate:list=[0,0], \
                ZIP=[0.0, 0.0 ,1.0], vset=0.0, iloss=0, pqcostRatio=100, \
                is_slack:bool=False, fail_rate_per_year:float=0.5, \
                outage_time:float=8):
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
        self.tolinelist = list()
        self.fromlinelist = list()
        self.nextbus = list()
        self.connected_lines = list()
        self.parent_network = None
        Bus.busCount += 1

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_per_year # failures per year
        self.fail_rate_per_hour = self.fail_rate_per_year/(365*24)
        self.outage_time = outage_time # hours
        self.cost = 0 # cost
        self.p_load_shed_stack = 0
        self.acc_p_load_shed = 0 # Accumulated load shed for bus
        self.q_load_shed_stack = 0
        self.acc_q_load_shed = 0
        
        

        ## Status attribute
        self.trafo_failed = False
        self.remaining_outage_time = 0
        
        ## Production and battery
        self.prod = None
        self.battery = None

        ## History
        self.history = {"pload":dict(), "qload":dict(), "pprod":dict(), "qprod":dict(), \
                        "remaining_outage_time":dict(), "trafo_failed":dict(), "p_load_shed_stack":dict(), \
                        "acc_p_load_shed":dict(), "q_load_shed_stack":dict(), \
                        "acc_q_load_shed":dict(), "voang":dict(), "vomag":dict(), \
                        "avg_fail_rate":dict(), "avg_annual_outage_time":dict(), "avg_outage_time":dict()}

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

    def reset_load(self):
        self.pload = 0
        self.qload = 0

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

    def trafo_fail(self, hour):
        """ 
        Trafo fails, load and generation is set to zero
        """
        self.trafo_failed = True
        self.remaining_outage_time = self.outage_time
        self.shed_load()
        if self.prod != None:
            self.prod.set_prod(0,0)
    
    def trafo_not_fail(self, hour):
        self.trafo_failed = False

    def get_battery(self):
        return self.battery

    def get_production(self):
        return self.prod

    def update_fail_status(self, hour):
        if self.trafo_failed:
            self.remaining_outage_time -= 1
            if self.remaining_outage_time == 0:
                self.trafo_not_fail(hour)
            else:
                self.shed_load()
                if self.prod != None:
                    self.prod.set_prod(0,0)

        else:
            p_fail = self.fail_rate_per_hour
            if self.ps_random.choice([True,False],p=[p_fail,1-p_fail]):
                self.trafo_fail(hour)
            else:
                self.trafo_not_fail(hour)

    def set_slack(self):
        self.is_slack = True
    
    def print_status(self):
        print("name: {:3s}, trafo_failed={}, pload={:.4f}, " \
            "is_slack={}".format(self.name, self.trafo_failed, self.pload, self.is_slack))#, toline={}, fromline={}, tolinelist={}, " \
            #"fromlinelist={}, connected_lines={}, cost={:.4f}"\, \
                    # self.toline if self.toline==None else self.toline.name, self.fromline if self.fromline == None else self.fromline.name,\
                    # self.tolinelist, self.fromlinelist, self.connected_lines, self.cost))

    def update_history(self, hour):
        self.acc_p_load_shed += self.p_load_shed_stack  # Update accumulated load shed for bus
        self.acc_q_load_shed += self.q_load_shed_stack
        self.history["pload"][hour] = self.pload
        self.history["qload"][hour] = self.qload
        self.history["pprod"][hour] = self.pprod
        self.history["qprod"][hour] = self.qprod
        self.history["remaining_outage_time"][hour] = self.remaining_outage_time
        self.history["trafo_failed"][hour] = self.trafo_failed
        self.history["p_load_shed_stack"][hour] = self.p_load_shed_stack
        self.history["acc_p_load_shed"][hour] = self.acc_p_load_shed
        self.history["q_load_shed_stack"][hour] = self.q_load_shed_stack
        self.history["acc_q_load_shed"][hour] = self.acc_q_load_shed
        self.history["voang"][hour] = self.voang
        self.history["vomag"][hour] = self.vomag
        self.history["avg_fail_rate"][hour] = self.get_avg_fail_rate() # Average failure rate (lamda_s)
        self.history["avg_annual_outage_time"][hour] = self.get_annual_outage_time() # Average annual outage time (U_s)
        self.history["avg_outage_time"][hour] = self.get_avg_outage_time() # Average outage time (r_s)
        self.clear_load_shed_stack()

    def get_history(self, attribute:str):
        return self.history[attribute]

    def set_cost(self, cost:float):
        self.cost = cost
    
    def get_cost(self):
        return self.cost

    def shed_load(self):
        self.p_load_shed_stack += self.pload
        self.q_load_shed_stack += self.qload
        self.reset_load()

    def clear_load_shed_stack(self):
        self.p_load_shed_stack = 0
        self.q_load_shed_stack = 0

    def add_random_seed(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

    def get_avg_fail_rate(self):
        """
        Returns the average failure rate of the bus
        """
        avg_fail_rate = self.fail_rate_per_hour
        if self.parent_network is not None:
            for line in self.parent_network.get_lines():
                avg_fail_rate += line.fail_rate_per_hour
        return avg_fail_rate

    def get_annual_outage_time(self):
        """
        Returns an estimate of the annual outage time of the bus
        """
        outage_time = 0
        shed_dict = self.history["p_load_shed_stack"] # Ignore reactive load shedding
        days = len(shed_dict)
        for shed_value in shed_dict.values():
            if shed_value > 1E-3: # Add tolerance
                outage_time += 1
        return outage_time/days*365

    def get_avg_outage_time(self):
        """
        Returns the average outage time of the bus
        """
        outage_time = 0
        shed_dict = self.history["p_load_shed_stack"] # Ignore reactive load shedding
        days = len(shed_dict)
        for shed_value in shed_dict.values():
            if shed_value > 1E-3: # Add tolerance
                outage_time += 1
        return outage_time/days

if __name__=="__main__":
    pass