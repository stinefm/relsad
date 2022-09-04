import matplotlib.lines as mlines
import numpy as np

from relsad.load.bus import CostFunction
from relsad.StatDist import StatDist, StatDistType, UniformParameters
from relsad.Time import Time, TimeUnit
from relsad.utils import (
    convert_yearly_fail_rate,
    interpolate,
    random_choice,
    eq,
)

from .Component import Component


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
    s_ref : float
        Apperent power reference [MVa]
    cost : float
        The energy shedding cost of the bus
    cost_functions : list
        List of power load cost functions
    pload_data : list
        List of active power load data
    qload_data : list
        List of reactive power load data
    ZIP : list
        List showing the ZIP load model
    p_load_downstream : float
        Active accumulated power load at node
    q_load_downstream : float
        Reactive accumulated power load at node
    p_loss_downstream : float
        Active accumulated power line loss at node
    q_loss_downstream : float
        Reactive accumulated power line loss at node
    voang : float
        Voltage angle [rad]
    vomag : float
        Voltage magnitude pu
    pload : float
        The active power load at the bus [MW]
    qload : float
        The reactive power load at the bus [MVar]
    pload_pu : float
        The active power load at the bus in pu
    qload_pu : float
        The reactive power load at the bus in pu
    pprod : float
        The active generated power at the bus [MW]
    qprod : float
        The reactive generated power at the bus [MVar]
    pprod_pu : float
        The active generated power at the bus in pu
    qprod_pu : float
        The reactive generated power at the bus in pu
    is_slack : bool
        Tells if the given bus is a slack bus or not
    toline : Line
        Tells which line that is going into the bus
    fromline : Line
        Tells which line that is going out of the bus
    toline_list : list
        List of lines going into the bus
    fromline_list : list
        List of lines going from the bus
    nextbus : List
        List of neighbor buses
    connected_lines : List
        List of connected lines
    parent_network : PowerNetwork
        Parent network of the bus
    fail_rate_per_year : float
        The failure rate per year for the transformer at the bus
    repair_time_dist : StatDist
        The repair time of the transformer at the bus [hours/fault]
    p_energy_shed_stack : float
        The amount of shedded active energy at the bus
        in the current sequence
    q_energy_shed_stack : float
        The amount of shedded reactive energy at the bus
        in the current sequence
    acc_p_energy_shed : float
        The accumulated amount of shedded active energy at the bus
        for the entire simulation
    acc_q_energy_shed : float
        The accumulated amount of shedded reactive energy at the bus
        for the entire simulation
    acc_outage_time : Time
        The accumulated outage time of the transformer at the bus
        for the entire simulation
    avg_fail_rate : float
        The average failure rate of the transformer at the bus
        for the entire simulation
    avg_outage_time : Time
        The average outage time of the transformer at the bus
        for the entire simulation
    num_consecutive_interruptions : float
        The current number of consecutive interruptions the bus experiences
    interruption_fraction : float
        The current fraction of interruption experienced by the bus
    curr_interruptions : float
        Current number of interruptions experienced by the bus
    acc_interruptions : float
        Accumulated number of interruptions experienced by the bus
    trafo_failed : bool
        Failure status of the transformer
    remaining_outage_time : Time
        The remaining outage time of the bus
    prod : Production
        The Production unit at the bus
    ev_park : EVPark
        The EVPark at the bus
    battery : Battery
        The Battery unit at the bus
    history : dict
        Dictonary that stores the sequential simulation history variables
    monte_carlo_history : dict
        Dictonary that stores the Monte Carlo simulation history variables


    Methods
    ----------
    reset_load_and_production_attributes()
        Resets the load and generation at the bus
    reset_load()
        Resets the load at the bus by setting the load to 0
    reset_prod()
        Resets the generation at the bus by setting the generation to 0
    add_load_data(pload_data, qload_data, cost_function)
        Adds load data to the bus
    prepare_load_data(time_indices)
        Prepares the load data for the current time step configuration
    add_load(pload, qload)
        Adds load to the bus
    set_load_and_cost(inc_idx)
        Sets the bus load and cost in MW based on load and cost profiles in the current increment
    get_load()
        Retuns the current load at the bus in MW
    draw_repair_time(dt)
        Decides and returns the repair time of the trafo based on a statistical distribution
    trafo_fail(dt)
        Sets the transformer status to failed, load and generation at the node are set to zero
    trafo_not_fail()
        Sets the transformer to not failed
    get_battery()
        Returns the battery at the bus
    get_production()
        Returns the generation unit at the bus
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
        Sets the specificed interruption cost related to Cost of Energy Not Supplied at the bus
    get_cost()
        Returns the specificed interruption cost related to Cost of Energy Not Supplied at the bus
    shed_load(dt)
        Sheds load at the bus and resets the load. The shedded load is added to a stack for the bus
    clear_energy_shed_stack()
        Resets the energy.shed stack for the bus
    add_random_instance(random_gen)
        Adds global random seed
    get_avg_fail_rate(curr_time)
        Returns the average failure rate of the transformer at the bus
    reset_status(save_flag)
        Resets and sets the status of the class parameters
    add_to_energy_shed_stack(p_load, q_load, dt)
        Adds the shedded load to the energy.shed stack at the bus
    reset_load_flow_data()
        Resets the variables used in the load flow analysis
    get_monte_carlo_history(attribute)
        Returns a specified history variable from the Monte Carlo simulation
    """

    ## Visual attributes
    marker = "|"
    size = 4**2
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
        is_slack: bool = False,
        fail_rate_per_year: float = 0.0,
        repair_time_dist: StatDist = StatDist(
            stat_dist_type=StatDistType.UNIFORM_FLOAT,
            parameters=UniformParameters(
                min_val=0.0,
                max_val=0.0,
            ),
        ),
    ):

        ## Informative attributes
        self.name = name
        self.n_customers = n_customers
        self.coordinate = coordinate

        ## Power flow attributes
        self.s_ref = s_ref
        self.cost = 0  # cost
        self.cost_functions = []
        self.pload_data = []
        self.qload_data = []
        self.ZIP = ZIP
        self.p_load_downstream = 0.0  # Active accumulated load at node
        self.q_load_downstream = 0.0  # Reactive accumulated load at node
        self.p_loss_downstream = 0.0  # Active accumulated line loss at node
        self.q_loss_downstream = 0.0  # Active accumulated line loss at node
        self.voang = 0.0
        self.vomag = 1.0
        self.pload = 0
        self.qload = 0
        self.pload_pu = 0
        self.qload_pu = 0
        self.pprod = 0
        self.qprod = 0
        self.pprod_pu = 0
        self.qprod_pu = 0

        ## Topological attributes
        self.is_slack = is_slack
        self.toline = None
        self.fromline = None
        self.toline_list = list()
        self.fromline_list = list()
        self.nextbus = list()
        self.connected_lines = list()
        self.parent_network = None

        ## Reliabilility attributes
        self.fail_rate_per_year = fail_rate_per_year  # failures per year
        self.repair_time_dist = repair_time_dist
        self.p_energy_shed_stack = 0
        self.q_energy_shed_stack = 0
        self.acc_p_energy_shed = 0
        self.acc_q_energy_shed = 0
        self.acc_outage_time = Time(0)
        self.avg_fail_rate = 0
        self.avg_outage_time = Time(0)
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0

        ## Status attribute
        self.trafo_failed = False
        self.remaining_outage_time = Time(0)

        ## Production, EV park and battery
        self.prod = None
        self.ev_park = None
        self.battery = None

        ## History
        self.history = {}
        self.monte_carlo_history = {}
        self.initialize_history()

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

        Parameters
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

        Parameters
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

        Parameters
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

    def add_load_data(
        self,
        pload_data: np.ndarray,
        qload_data: np.ndarray = None,
        cost_function: CostFunction = CostFunction(A=1, B=0),
    ):
        """
        Adds load data to the bus

        Parameters
        ----------
        pload_data : np.ndarray
            Active power load array
        qload_data : np.ndarray
            Reactive power load array
        cost_function : CostFunction
            Load cost function

        Returns
        ----------
        None

        """
        self.cost_functions.append(cost_function)
        self.pload_data.append(pload_data)
        if qload_data is None:
            self.qload_data.append(np.zeros_like(pload_data))
        else:
            self.qload_data.append(qload_data)

    def prepare_load_data(
        self,
        time_indices: np.ndarray,
    ):
        """
        Prepares the load data for the current time step configuration

        Parameters
        ----------
        time_indices : np.ndarray
            Time indices used to discretize the load data

        Returns
        ----------
        None

        """
        for i, pload_array in enumerate(self.pload_data):
            self.pload_data[i] = interpolate(
                array=pload_array,
                time_indices=time_indices,
            )
        for i, qload_array in enumerate(self.qload_data):
            self.qload_data[i] = interpolate(
                array=qload_array,
                time_indices=time_indices,
            )

    def add_load(
        self,
        pload: float,
        qload: float,
    ):
        """
        Adds load to the bus

        Parameters
        ----------
        pload : float
            Active power
        qload : float
            Reactive power

        Returns
        ----------
        None

        """
        # MW and MVar
        self.pload += pload
        self.qload += qload
        # Per unit
        self.pload_pu = self.pload / self.s_ref
        self.qload_pu = self.qload / self.s_ref

    def set_load_and_cost(self, inc_idx: int):
        """
        Sets the bus load and cost in MW based on load and cost profiles
        in the current increment

        Parameters
        ----------
        inc_idx : int
            Index of the current increment

        Returns
        ----------
        None

        """
        self.reset_load()
        default_cost = 1e8
        type_cost = 0
        for i, cost_function in enumerate(self.cost_functions):
            if (
                not self.pload_data[i] is None
                and not self.qload_data[i] is None
            ):
                type_cost = max(
                    type_cost,
                    cost_function.A + cost_function.B * 1,
                )
                self.add_load(
                    pload=self.pload_data[i][inc_idx] * self.n_customers,
                    qload=self.qload_data[i][inc_idx] * self.n_customers,
                )
        if type_cost > 0:
            self.set_cost(type_cost)
        else:
            self.set_cost(default_cost)

    def get_load(self):
        """
        Returns the current load at the bus in MW

        Parameters
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

    def draw_repair_time(self, dt: Time):
        """
        Decides and returns the repair time of the trafo based on a statistical distribution

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        return Time(
            self.repair_time_dist.draw(
                random_instance=self.ps_random,
                size=1,
            )[0],
            dt.unit,
        )

    def trafo_fail(self, dt: Time):
        """
        Sets the transformer status to failed, load and generation at the bus are set to zero

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        self.trafo_failed = True
        self.remaining_outage_time = self.draw_repair_time(dt)
        self.shed_load(dt)
        if self.prod is not None:
            self.prod.reset_prod()

    def trafo_not_fail(self):
        """
        Sets the transformer status to not failed

        Parameters
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

        Parameters
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
        Returns the generation unit at the bus

        Parameters
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
        Updates the fail status of the transformer.
        Sets the fail status to failed if the transformer is failed
        or the fail status to not failed if the transformer is not failed

        Parameters
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
                self.remaining_outage_time = Time(0)
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

        Parameters
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

        Parameters
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

        Parameters
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
        self.history["p_energy_shed_stack"] = {}
        self.history["acc_p_energy_shed"] = {}
        self.history["q_energy_shed_stack"] = {}
        self.history["acc_q_energy_shed"] = {}
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

        Parameters
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
        # Update accumulated energy.shed for bus
        self.acc_p_energy_shed += self.p_energy_shed_stack
        self.acc_q_energy_shed += self.q_energy_shed_stack
        dt = curr_time - prev_time if prev_time is not None else curr_time
        self.acc_outage_time += dt if self.p_energy_shed_stack > 0 else Time(0)
        self.avg_outage_time = (
            Time(
                self.acc_outage_time / curr_time, curr_time.unit
            )
            if curr_time != Time(0, curr_time.unit)
            else Time(0, curr_time.unit)
        )
        self.avg_fail_rate = self.get_avg_fail_rate(curr_time)
        # Accumulate fraction of interupted customers
        self.interruption_fraction = (
            self.p_energy_shed_stack / (self.pload * dt.get_hours())
            if not eq(self.pload, 0) and dt.get_hours() > 0
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
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["pload"][time] = self.pload
            self.history["qload"][time] = self.qload
            self.history["pprod"][time] = self.pprod
            self.history["qprod"][time] = self.qprod
            self.history["remaining_outage_time"][
                time
            ] = self.remaining_outage_time.get_unit_quantity(curr_time.unit)
            self.history["trafo_failed"][time] = self.trafo_failed
            self.history["p_energy_shed_stack"][
                time
            ] = self.p_energy_shed_stack
            self.history["acc_p_energy_shed"][
                time
            ] = self.acc_p_energy_shed
            self.history["q_energy_shed_stack"][
                time
            ] = self.q_energy_shed_stack
            self.history["acc_q_energy_shed"][
                time
            ] = self.acc_q_energy_shed
            self.history["voang"][time] = self.voang
            self.history["vomag"][time] = self.vomag
            self.history["avg_fail_rate"][
                time
            ] = self.avg_fail_rate  # Average failure rate (lamda_s)
            self.history["avg_outage_time"][
                time
            ] = self.avg_outage_time.get_unit_quantity(
                curr_time.unit
            )  # Average outage time (r_s)
            self.history["acc_outage_time"][
                time
            ] = self.acc_outage_time.get_unit_quantity(
                curr_time.unit
            )  # Accumulated outage time
            self.history["interruption_fraction"][
                time
            ] = self.interruption_fraction
            self.history["acc_interruptions"][
                time
            ] = self.acc_interruptions
        self.clear_energy_shed_stack()

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
        Sets the specificed interruption cost related to Cost of Energy Not Supplied at the bus

        Parameters
        ----------
        cost : float
            The specificed interruption cost

        Returns
        ----------
        None

        """
        self.cost = cost

    def get_cost(self):
        """
        Returns the specificed interruption cost related to Cost of Energy Not Supplied at the bus

        Parameters
        ----------
        None

        Returns
        ----------
        cost : float
            The specificed interruption cost

        """
        return self.cost

    def shed_load(self, dt: Time):
        """
        Sheds load at the bus and resets the load. The shedded load is added to a stack for the bus

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        self.add_to_energy_shed_stack(
            self.pload,  # MW
            self.qload,  # MW
            dt,
        )
        self.reset_load()

    def clear_energy_shed_stack(self):
        """
        Resets the energy.shed stack for the bus

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.p_energy_shed_stack = 0
        self.q_energy_shed_stack = 0

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

    def get_avg_fail_rate(self, curr_time: Time):
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
        fail_rate = self.fail_rate_per_year
        if self.parent_network is not None:
            for line in self.parent_network.get_lines():
                fail_rate += line.fail_rate_per_year
        avg_fail_rate = (
            fail_rate / curr_time.get_years()
            if curr_time.get_years() > 0
            else 0
        )
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
        self.clear_energy_shed_stack()
        # Accumulated energy.shed for bus
        self.acc_p_energy_shed = 0
        self.acc_q_energy_shed = 0
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0
        if save_flag:
            self.initialize_history()

    def add_to_energy_shed_stack(self, p_load: float, q_load: float, dt: Time):
        """
        Adds the shedded load to the energy.shed stack at the bus

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
        self.p_energy_shed_stack += p_load * dt.get_hours()  # MWh
        self.q_energy_shed_stack += q_load * dt.get_hours()  # MWh

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
