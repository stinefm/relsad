import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from relsad.utils import (
    random_choice,
    convert_yearly_fail_rate,
)

from relsad.Time import (
    Time,
    TimeUnit,
)


class Bus(Component):
    """
    Common base class for all distribution buses

    ...

    Attributes
    ----------
    name : string
        Name of the bus
    n_customers : int
        Number of customers connected to that bus
    coordinate : list
        Coordinate of the bus
    ZIP : list
        Type of load model
    s_ref : float
        Apperent power reference [MVa]
    vset : float
    iloss : float
    pqcostRatio : float
    is_slack : bool
        Tells if the given bus is a slack bus or not
    fail_rate_per_year : float
        The failure rate of the transformer on the bus per year
    outage_time : Time
        The outage time of the transformer on the bus
    calc_sensitivities : bool
        Sets the calculation of sensitivities in the load flow on/off
    load_dict : dict
        Dictionary with the load at the bus
    comp : int
    num : 
    toline : Line 
        Tells which line/lines that are going into the bus
    fromline : Line
        Tells which line/lines that are going out of the bus
    toline_list : list
        List of lines going into the bus
    pload : float
        The active load at the bus [MW]
    qload : float
        The reactive load at the bus [MVar]
    ZIP : list
        List showing the ZIP load model
    vset : float
    iloss : float
    pqcostRatio :
    comp :
    p_load_downstream : float
    q_load_downstream : float
    p_loss_downstream : float
    q_loss_downstream : float
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

    Methods
    ----------
    reset_load_and_production_attributes()
        Resets the load and generation at the bus
    reset_load()
        Resets the load at the bus by setting the load to 0
    reset_prod()
        Resets the generation at the bus by setting the generation to 0
    add_load_dict(load_dict)
        Adds a load dictionary to the bus
    set_load(inc_idx)
        Sets the bus load in MW based on load profile
    get_load()
        Retuns the current load at the bus in MW
    trafo_fail(dt)
        Sets the transformer status to failed, load and generation at the node are set to zero
    trafo_not_fail()
        Sets the transformer to not failed
    get_battery()
        Returns the battery at the bus
    get_production()   
        Returns the generation at the bus
    update_fail_status(dt)
        Updates the fail status of the transformer. Sets the fail status to failed if the transformer is failed or the fail status to not failed if the transformer is not failed
    set_slack()
        Sets a bus to slack bus
    print_status()
        Prints the status of the bus
    initialize_history()
        Initializes the history variables
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute at the bus
    set_cost(cost)
        Sets the Cost of Energy Not Supplied at the bus
    get_cost()
        Returns the Cost of Energy Not Supplied at the bus
    shed_load(dt)
        Sheds load at the bus and resets the load. The shedded load is added to a stack for the bus
    clear_load_shed_stack()
        Resets the load shed stack for the bus
    add_random_instance(random_gen)
        Adds global random seed
    get_avg_fail_rate()
        Returns the average failure rate of the transformer at the bus
    reset_status(save_falg)
        Resets and sets the status of the class parameters
    add_to_load_shed_stack(p_load, q_load, dt)
        Adds the shedded load to the load shed stack at the bus
    reset_load_flow_data()
        Resets the variables used in the load flow analysis
    get_monte_carlo_history(attribute)
        Returns a specified history variable from the Monte Carlo simulation
    """

    busCount = 0

    ## Visual attributes
    marker = "|"
    size = 4 ** 2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=2,
        markersize=size,
        linestyle="None",
    )

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        n_customers: int = 1,
        coordinate: list = [0, 0],
        ZIP=[0.0, 0.0, 1.0],
        s_ref: float = 1,  # MVA
        vset : float = 0.0,
        iloss: float = 0,
        pqcostRatio=100,
        is_slack: bool = False,
        fail_rate_per_year: float = 0.007,
        outage_time: Time = Time(8, TimeUnit.HOUR),
        calc_sensitivities: bool = False,
    ):
        ## Informative attributes
        self.name = name
        self.n_customers = n_customers
        self.coordinate = coordinate

        ## Power flow attributes
        self.s_ref = s_ref
        self.load_dict = dict()
        self.ZIP = ZIP
        self.vset = vset
        self.iloss = iloss
        self.pqcostRatio = pqcostRatio
        self.calc_sensitivities = calc_sensitivities
        self.comp = 0
        self.reset_load_flow_data()

        ## Topological attributes
        self.num = Bus.busCount
        self.is_slack = is_slack
        self.toline = None
        self.fromline = None
        self.toline_list = list()
        self.fromline_list = list()
        self.nextbus = list()
        self.connected_lines = list()
        self.parent_network = None
        Bus.busCount += 1

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_per_year  # failures per year
        self.outage_time = outage_time  # hours
        self.acc_outage_time = Time(0)
        self.avg_fail_rate = 0
        self.avg_outage_time = Time(0)
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0

        ## Production, EV park and battery
        self.prod = None
        self.ev_park = None
        self.battery = None

        ## History
        self.history = {}
        self.monte_carlo_history = {}

        self.reset_status(True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Bus(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Bus)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def reset_load_and_prod_attributes(self):
        """
        Resets the load and generation at the bus

        Paramters
        ----------
        None

        Returns
        ----------
        None

        """
        self.reset_load()
        self.reset_prod()

    def reset_load(self):
        """
        Resets the load at the bus by setting the load to 0

        Paramters
        ----------
        None

        Returns
        ----------
        None

        """
        self.pload = 0
        self.qload = 0
        self.pload_pu = 0
        self.qload_pu = 0

    def reset_prod(self):
        """
        Resets the generation at the bus by setting the generation to 0

        Paramters
        ----------
        None

        Returns
        ----------
        None
        
        """
        self.pprod = 0
        self.qprod = 0
        self.pprod_pu = 0
        self.qprod_pu = 0

    def add_load_dict(self, load_dict: dict):
        """
        Adds a load dictionary to the bus

        Paramters
        ----------
        load_dict : dict
            Dictionary with the load at the bus

        Returns
        ----------
        None
        
        """
        self.load_dict = load_dict

    def set_load(self, inc_idx: int):
        """
        Sets the bus load in MW based on load profile

        Paramters
        ----------
        inc_idx : int
            Dictionary with the load at the bus

        Returns
        ----------
        None
        
        """
        self.reset_load()
        if self.load_dict:
            for load_type in self.load_dict["load"]:
                try:
                    type_cost = self.load_dict["cost"][load_type]
                    A = type_cost["A"]
                    B = type_cost["B"]
                    self.set_cost(A + B * 1)
                    self.pload += (
                        self.load_dict["load"][load_type]["pload"][inc_idx]
                        * self.n_customers
                    )
                    self.qload += (
                        self.load_dict["load"][load_type]["qload"][inc_idx]
                        * self.n_customers
                    )
                except KeyError:
                    print(
                        "Load type {} is not in cost_functions".format(
                            load_type
                        )
                    )
        else:
            self.set_cost(1e8)
        self.pload_pu = self.pload / self.s_ref
        self.qload_pu = self.qload / self.s_ref

    def get_load(self):
        """
        Returns the current load at the bus in MW

        Paramters
        ----------
        None

        Returns
        ----------
        pload : float
            The active load at the bus
        qload : float
            The reactive load at the bus
        
        """
        return self.pload, self.qload

    def trafo_fail(self, dt: Time):
        """
        Sets the transformer status to failed, load and generation at the bus are set to zero

        Paramters
        ----------
        dt : Time 
            The current time step

        Returns
        ----------
        None
        
        """
        self.trafo_failed = True
        self.remaining_outage_time = self.outage_time
        self.shed_load(dt)
        if self.prod is not None:
            self.prod.reset_prod()

    def trafo_not_fail(self):
        """
        Sets the transformer status to not failed

        Paramters
        ----------
        None

        Returns
        ----------
        None
        
        """
        self.trafo_failed = False

    def get_battery(self):
        """
        Returns the battery at the bus

        Paramters
        ----------
        None
        
        Returns
        ----------
        battery : Battery
            Returns the battery at the bus, none if there is no battery at the bus
        
        """
        return self.battery

    def get_production(self):
        """
        Returns the generation at the bus

        Paramters
        ----------
        None

        Returns
        ----------
        prod : Production
            Returns the generation at the bus, none if there is no battery at the bus
        
        """
        return self.prod

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status of the transformer. Sets the fail status to failed if the transformer is failed or the fail status to not failed if the transformer is not failed

        Paramters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None
        
        """
        if self.trafo_failed:
            self.remaining_outage_time -= dt
            if self.remaining_outage_time <= Time(0):
                self.trafo_not_fail()
            else:
                self.shed_load(dt)
                if self.prod is not None:
                    self.prod.reset_prod()
        else:
            p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
            if random_choice(self.ps_random, p_fail):
                self.trafo_fail(dt)
            else:
                self.trafo_not_fail()

    def set_slack(self):
        """
        Sets a bus to slack bus

        Paramters
        ----------
        None

        Returns
        ----------
        None
        
        """
        self.is_slack = True

    def print_status(self):
        """
        Prints the status of the bus 

        Paramters
        ----------
        None

        Returns
        ----------
        None
        
        """
        print(
            "name: {:3s}, trafo_failed={}, pload={:.4f}, "
            "is_slack={}".format(
                self.name, self.trafo_failed, self.pload, self.is_slack
            )
        )

    def initialize_history(self):
        """
        Initializes the history variables 

        Paramters
        ----------
        None

        Returns
        ----------
        None
        
        """
        self.history["pload"] = {}
        self.history["qload"] = {}
        self.history["pprod"] = {}
        self.history["qprod"] = {}
        self.history["remaining_outage_time"] = {}
        self.history["trafo_failed"] = {}
        self.history["p_load_shed_stack"] = {}
        self.history["acc_p_load_shed"] = {}
        self.history["q_load_shed_stack"] = {}
        self.history["acc_q_load_shed"] = {}
        self.history["voang"] = {}
        self.history["vomag"] = {}
        self.history["avg_fail_rate"] = {}
        self.history["avg_outage_time"] = {}
        self.history["acc_outage_time"] = {}
        self.history["interruption_fraction"] = {}
        self.history["acc_interruptions"] = {}

    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        """
        Updates the history variables 

        Paramters
        ----------
        prev_time : Time
            The previous time
        curr_time : Time
            Current time
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None
        
        """
        # Update accumulated load shed for bus
        self.acc_p_load_shed += self.p_load_shed_stack
        self.acc_q_load_shed += self.q_load_shed_stack
        dt = curr_time - prev_time if prev_time is not None else curr_time
        self.acc_outage_time += dt if self.p_load_shed_stack > 0 else Time(0)
        self.avg_outage_time = Time(self.acc_outage_time / curr_time, curr_time.unit)
        self.avg_fail_rate = self.get_avg_fail_rate()
        # Accumulate fraction of interupted customers
        self.interruption_fraction = (
            self.p_load_shed_stack / (self.pload * dt.get_hours())
            if self.pload != 0
            else 0
        )

        if self.interruption_fraction > 0:
            self.curr_interruptions += self.interruption_fraction
            self.num_consecutive_interruptions += 1
        else:
            if self.num_consecutive_interruptions >= 1:
                self.acc_interruptions += (
                    self.curr_interruptions
                    / self.num_consecutive_interruptions
                )
            self.curr_interruptions = 0
            self.num_consecutive_interruptions = 0

        if save_flag:
            self.history["pload"][curr_time] = self.pload
            self.history["qload"][curr_time] = self.qload
            self.history["pprod"][curr_time] = self.pprod
            self.history["qprod"][curr_time] = self.qprod
            self.history["remaining_outage_time"][
                curr_time
            ] = self.remaining_outage_time.get_unit_quantity(curr_time.unit)
            self.history["trafo_failed"][curr_time] = self.trafo_failed
            self.history["p_load_shed_stack"][
                curr_time
            ] = self.p_load_shed_stack
            self.history["acc_p_load_shed"][curr_time] = self.acc_p_load_shed
            self.history["q_load_shed_stack"][
                curr_time
            ] = self.q_load_shed_stack
            self.history["acc_q_load_shed"][curr_time] = self.acc_q_load_shed
            self.history["voang"][curr_time] = self.voang
            self.history["vomag"][curr_time] = self.vomag
            self.history["avg_fail_rate"][
                curr_time
            ] = self.get_avg_fail_rate()  # Average failure rate (lamda_s)
            self.history["avg_outage_time"][
                curr_time
            ] = self.avg_outage_time.get_unit_quantity(
                curr_time.unit
            )  # Average outage time (r_s)
            self.history["acc_outage_time"][
                curr_time
            ] = self.acc_outage_time.get_unit_quantity(
                curr_time.unit
            )  # Accumulated outage time
            self.history["interruption_fraction"][
                curr_time
            ] = self.interruption_fraction
            self.history["acc_interruptions"][
                curr_time
            ] = self.acc_interruptions
        self.clear_load_shed_stack()

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute at the bus

        Parameters
        ----------
        attribute : str
            Bus attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute
        """
        return self.history[attribute]

    def set_cost(self, cost: float):
        """
        Sets the Cost of Energy Not Supplied at the bus

        Paramters
        ----------
        cost : float
            The Cost of Energy Not Supplied

        Returns
        ----------
        None
        
        """
        self.cost = cost

    def get_cost(self):
        """
        Returns the Cost of Energy Not Supplied at the bus

        Paramters
        ----------
        None

        Returns
        ----------
        cost : float
            The Cost of Energy Not Supplied
        
        """
        return self.cost

    def shed_load(self, dt: Time):
        """
        Sheds load at the bus and resets the load. The shedded load is added to a stack for the bus

        Paramters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None
        
        """
        self.add_to_load_shed_stack(
            self.pload,  # MW
            self.qload,  # MW
            dt,
        )
        self.reset_load()

    def clear_load_shed_stack(self):
        """
        Resets the load shed stack for the bus

        Paramters
        ----------
        None

        Returns
        ----------
        None
        
        """
        self.p_load_shed_stack = 0
        self.q_load_shed_stack = 0

    def add_random_instance(self, random_gen):
        """
        Adds global random seed

        Parameters
        ----------
        random_gen : int
            Random number generator

        Returns
        ----------
        None

        """
        self.ps_random = random_gen

    def get_avg_fail_rate(self):
        """
        Returns the average failure rate of the transformer at the bus

        Parameters
        ----------
        None

        Returns
        ----------
        avg_fail_rate : float
            The average failure rate of the transformer at the bus

        """
        avg_fail_rate = self.fail_rate_per_year
        if self.parent_network is not None:
            for line in self.parent_network.get_lines():
                avg_fail_rate += line.fail_rate_per_year
        return avg_fail_rate

    def reset_status(self, save_flag: bool):
        """
        Resets and sets the status of the class parameters

        Parameters
        ----------
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        self.trafo_failed = False
        self.remaining_outage_time = Time(0)
        self.acc_outage_time = Time(0)
        self.reset_load_and_prod_attributes()
        self.cost = 0  # cost
        self.clear_load_shed_stack()
        # Accumulated load shed for bus
        self.acc_p_load_shed = 0
        self.acc_q_load_shed = 0
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0
        if save_flag:
            self.initialize_history()

    def add_to_load_shed_stack(self, p_load: float, q_load: float, dt: Time):
        """
        Adds the shedded load to the load shed stack at the bus

        Parameters
        ----------
        p_load : float
            The active power at the bus
        q_load : float
            The reactive power at the bus
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        #if self.battery is None:
        self.p_load_shed_stack += p_load * dt.get_hours()  # MWh
        self.q_load_shed_stack += q_load * dt.get_hours()  # MWh

    def reset_load_flow_data(self):
        """
        Resets the variables used in the load flow analysis

        Parameters
        ---------
        None

        Returns
        --------
        None
        """
        self.p_load_downstream = 0.0  # Active accumulated load at node
        self.q_load_downstream = 0.0  # Reactive accumulated load at node
        self.p_loss_downstream = 0.0  # Active accumulated line loss at node
        self.q_loss_downstream = 0.0  # Active accumulated line loss at node
        self.dPdV = 0.0  # Disse trengs ikke. Blir egentlig kun regnet ut i siste iterasjon av en last flyt, kan derfor lage en egen funksjon ut av dette som kun kjører dette når man skal ta siste iterasjona av en last flyt.
        self.dQdV = 0.0
        self.dVdP = 0.0
        self.dVdQ = 0.0
        self.dPlossdP = 0.0
        self.dPlossdQ = 0.0
        self.dQlossdP = 0.0
        self.dQlossdQ = 0.0
        self.dP2lossdP2 = 1.0  # To be able to run the voltage optimization also in the first iteration
        self.dP2lossdQ2 = 1.0  # To be able to run the voltage optimization also in the first iteration
        self.lossRatioP = 0.0
        self.lossRatioQ = 0.0
        self.voang = 0.0
        self.vomag = 1.0

    def get_monte_carlo_history(self, attribute):
        """
        Returns a specified history variable from the Monte Carlo simulation

        Parameters
        ---------
        attribute : str
            Bus attribute

        Returns
        --------
        monte_carlo_history[attribute] : str
            The specified history variable from the Monte Carlo simulation
        """
        return self.monte_carlo_history[attribute]
