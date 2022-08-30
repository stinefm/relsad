import matplotlib.lines as mlines
import numpy as np

from relsad.Table import Table
from relsad.Time import Time, TimeUnit

from .Battery import Battery, BatteryType
from .Bus import Bus
from .Component import Component
from .MicrogridController import MicrogridMode


class EVPark(Component):

    """
    Common class for batteries
    ...

    Attributes
    ----------
    name : string
        Name of the EV park
    bus : Bus
        The bus the EV park is connected to
    num_ev_dist : Table
        Statistical distribution that returns the amount of EVs available at a given time in the network
    inj_p_max : float
        The active power charging/discharging capacity of the EV battery [MW]
    inj_q_max : float
        The reactive power discharging capacity of the EV battery [MVar]
    E_max : float
        The maximum energy capacity of an EV [Mwh]
    SOC_min : float
        The minimal state of charge level in the EV battery
    SOC_max : float
        The maximum state of charge level in the EV battery
    n_battery : float
        The EV battery efficiency
    v2g_flag : bool
        A flag telling if the EV park contributes with V2G services or not
    curr_p_demand : float
        Current demand of active power from the EV park [MW]
    curr_q_demand : float
        Current demand of reactive power from the EV park [MVar]
    curr_p_charge : float
        Current active power that are being charged/dischared [MW]
    curr_q_charge : float
        Current reactive power that are being charged/dischared [MVar]
    available_cars : list
        List of available cars in the EV park
    available_num_cars : int
        Number of available cars in the EV park
    num_cars : int
        Number of cars in the EV park
    num_consecutive_interruptions : int
        Number of consecutive interruptions experienced by the EV park
    park_interruption_fraction : float
        Fraction of interruption experienced by the EV park
    acc_available_num_cars : int
        Accumulated available number of cars in EV park
    acc_num_interruptions : float
        Accumulated number of interruptions experienced by the EV park
    acc_exp_interruptions : float
        Accumulated experienced interruptions in the EV park
    curr_exp_interruptions : float
        Current experienced interruptions in the EV park
    acc_exp_car_interruptions : float
        Accumulated experienced car interruptions in the EV park
    curr_exp_car_interruptions : float
        Current experienced car interruptions in the EV park
    curr_interruption_duration : Time
        Current interruption duration experienced by the EV park
    acc_interruption_duration : Time
        Accumulated interruption duration experienced by the EV park
    history : dict
        Dictonary attribute that stores the historic variables

    Methods
    ----------
    draw_current_state(hour_of_day)
        Draws the number of EVs in the park at that time and the SOC level of each EV which will make the SOC level of the EV park
    update(p, q, fail_duration, dt, hour_of_day)
        Updates the EV park status for the current time step
    get_curr_demand(dt)
        Returns the current power demand of an EV
    get_SOC()
        Returns the SOC level of the EV park
    get_ev_index()
        Returns the power demand of av EV that is not met by the system
    initialize_history()
        Initializes the history variables
    update_history(prev_time, curr_time, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    update_fail_status(dt)
        Locks og unlocks the battery functionality based on failure states of the basestation
    add_random_instance(random_gen)
        Adds global random seed
    print_status()
        Prints the status of the EV park
    reset_status(save_flag)
        Resets and sets the status of the class parameters

    """

    ## Visual attributes
    marker = "x"
    size = 3**2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=1,
        markersize=size,
        linestyle="None",
    )

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        bus: Bus,
        num_ev_dist: Table,
        inj_p_max: float = 0.072,
        inj_q_max: float = 0.072,
        E_max: float = 0.70,
        SOC_min: float = 0.2,
        SOC_max: float = 0.9,
        n_battery: float = 0.95,
        v2g_flag: bool = True,
    ):

        # Verify input
        if bus is None:
            raise Exception("EVPark must be connected to a Bus")
        if bus.parent_network is not None:
            raise Exception(
                "EVPark must be created before the bus is connected to a network"
            )
        if num_ev_dist is None:
            raise Exception(
                "EVPark must have a table distributing the number"
                "of EV during the day"
            )
        if inj_p_max < 0:
            raise Exception("The active power injection must be positive")
        if inj_q_max < 0:
            raise Exception("The reactive power injection must be positive")
        if E_max < 0:
            raise Exception("The energy capacity must be positive")
        if SOC_min < 0 or SOC_max > 1:
            raise Exception("The SOC limits must be between 0 and 1")
        if n_battery < 0 or n_battery > 1:
            raise Exception("The efficiency must be between 0 and 1")

        self.name = name

        self.bus = bus
        bus.ev_park = self

        self.num_ev_dist = num_ev_dist
        self.inj_p_max = inj_p_max  # MW
        self.inj_q_max = inj_q_max  # MVar
        self.E_max = E_max  # MWh
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.n_battery = n_battery

        self.curr_p_demand = 0  # MW
        self.curr_q_demand = 0  # MVar
        # curr_p_charge < 0 => discharge
        # curr_p_charge > 0 => charge
        self.curr_p_charge = 0  # MW
        self.curr_q_charge = 0  # MVar

        self.v2g_flag = v2g_flag

        self.available_cars = list()
        self.available_num_cars = 0
        self.num_cars = round(max(self.num_ev_dist.y))

        ## Reliability attributes
        self.num_consecutive_interruptions = 0
        self.park_interruption_fraction = 0
        self.acc_available_num_cars = 0
        self.acc_num_interruptions = 0
        self.curr_exp_interruptions = 0
        self.acc_exp_interruptions = 0
        self.curr_exp_car_interruptions = 0
        self.acc_exp_car_interruptions = 0
        self.curr_interruption_duration = Time(0)
        self.acc_interruption_duration = Time(0)

        ## History
        self.history = {}
        self.initialize_history()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"EVPark(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, EVPark)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def draw_current_state(self, hour_of_day: int):
        """
        Draws the number of EVs in the park at that time
        and the SOC level of each EV which will make the SOC level of the EV park

        Parameters
        ----------
        hour_of_day : int
            The hour of the day
        Returns
        ----------
        None

        """
        # Draw number of cars in the EV park
        self.available_num_cars = round(
            self.num_ev_dist.get_value(hour_of_day)
        )

        # Draw the SOC states of the cars in the EV park
        soc_states = self.ps_random.uniform(
            low=self.SOC_min,
            high=self.SOC_max,
            size=self.available_num_cars,
        )

        # Create the current cars in the EV park with
        # their respective status
        self.available_cars = [
            Battery(
                name="ev{:d}_{}".format(i, self.name),
                bus=self.bus,
                inj_p_max=self.inj_p_max,
                inj_q_max=self.inj_q_max,
                E_max=self.E_max,
                SOC_min=self.SOC_min,
                SOC_max=self.SOC_max,
                n_battery=self.n_battery,
                battery_type=BatteryType.EV,
                random_instance=self.ps_random,
                SOC_start=soc_states[i],
            )
            for i in range(self.available_num_cars)
        ]

    def update(
        self,
        p: float,
        q: float,
        fail_duration: Time,
        dt: Time,
        hour_of_day: int,
    ):
        """
        Updates the EV park status for the current time step

        Parameters
        ----------
        p : float
            Active power balance of the parent power system
        q : float
            Reactive power balance of the parent power system
        fail_duration : Time
            The duration of the current failure
        dt : Time
            The current time step
        hour_of_day : int
            The hour of the day
        Returns
        ----------
        p : float
            Remaining active power balance of the parent power system
        q : float
            Remaining reactive power balance of the parent power system

        """
        if fail_duration == dt:
            self.draw_current_state(hour_of_day)
            self.acc_available_num_cars += self.available_num_cars

        # Update car batteries based on system balance
        p_start = p
        q_start = q
        for car in self.available_cars:
            if self.v2g_flag is True:
                # Vehicle to grid: allow charge and discharge
                p, q = car.update_bus_load_and_prod(p, q, dt)
            else:
                # Not vehicle to grid: allow charge only
                if p < 0:
                    p, q = car.update_bus_load_and_prod(p, q, dt)
        p_change = p_start - p
        q_change = q_start - q

        # Define load or production generated from the EV park
        pprod = max(0, p_change)
        qprod = max(0, q_change)
        pload = abs(min(0, p_change))
        qload = abs(min(0, q_change))

        # Update current demand and charge attributes
        (
            self.curr_p_demand,
            self.curr_q_demand,
        ) = self.get_curr_demand(dt)
        self.curr_p_charge = pload - pprod
        self.curr_q_charge = qload - qprod
        return p, q

    def get_curr_demand(self, dt: Time):
        """
        Returns the current power demand of an EV

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        curr_p_demand : float
            The current active power demand of the EV
        curr_p_demand : float
            The current reactive power demand of the EV

        """
        curr_p_demand = 0
        curr_q_demand = 0
        for car in self.available_cars:
            curr_p_demand += min(
                car.inj_p_max,
                (car.E_max * car.SOC_max - car.E_battery) / dt.get_hours(),
            )
        return curr_p_demand, curr_q_demand

    def get_SOC(self):
        """
        Returns the SOC level of the EV park

        Parameters
        ----------
        None

        Returns
        ----------
        mean_SOC: float
            The average SOC value of the EV park

        """

        if self.available_num_cars <= 0:
            return 0
        mean_SOC = np.mean([car.SOC for car in self.available_cars])
        return mean_SOC

    def get_ev_index(self):
        """
        Returns the power demand of an EV that is not met by the system

        Parameters
        ----------
        None

        Returns
        ----------
        ev_index: float
            The power demand of an EV that is not met by the system

        """
        ev_index = self.curr_p_demand - self.curr_p_charge
        return ev_index

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

        self.history["SOC"] = {}
        self.history["ev_index"] = {}
        self.history["demand"] = {}
        self.history["charge"] = {}
        self.history["num_cars"] = {}
        self.history["available_num_cars"] = {}
        self.history["park_interruption_fraction"] = {}
        self.history["acc_num_interruptions"] = {}
        self.history["acc_exp_interruptions"] = {}
        self.history["acc_exp_car_interruptions"] = {}
        self.history["acc_interruption_duration"] = {}
        self.history["acc_available_num_cars"] = {}

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
        dt = curr_time - prev_time if prev_time is not None else curr_time
        # Accumulate fraction of interupted customers
        self.curr_exp_car_interruptions = (
            abs(self.curr_p_charge / self.inj_p_max)
            if self.curr_p_charge < 0
            else 0
        )
        self.park_interruption_fraction = (
            self.curr_exp_car_interruptions / self.num_cars
        )

        if self.park_interruption_fraction > 0:
            self.curr_exp_interruptions += self.park_interruption_fraction
            self.num_consecutive_interruptions += 1
            self.curr_interruption_duration += dt
        else:
            if self.num_consecutive_interruptions >= 1:
                self.acc_num_interruptions += 1
                self.acc_exp_interruptions += (
                    self.curr_exp_interruptions
                    / self.num_consecutive_interruptions
                )
                self.acc_exp_car_interruptions += (
                    self.curr_exp_car_interruptions
                    / self.num_consecutive_interruptions
                )
                self.acc_interruption_duration += (
                    self.curr_interruption_duration
                )
            self.curr_exp_interruptions = 0
            self.curr_exp_car_interruptions = 0
            self.curr_interruption_duration = Time(0)
            self.num_consecutive_interruptions = 0
        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["SOC"][time] = self.get_SOC()
            self.history["ev_index"][time] = self.get_ev_index()
            self.history["demand"][time] = self.curr_p_demand
            self.history["charge"][time] = self.curr_p_charge
            self.history["num_cars"][time] = self.num_cars
            self.history["available_num_cars"][
                time
            ] = self.available_num_cars
            self.history["park_interruption_fraction"][
                time
            ] = self.park_interruption_fraction
            self.history["acc_num_interruptions"][
                time
            ] = self.acc_num_interruptions
            self.history["acc_exp_interruptions"][
                time
            ] = self.acc_exp_interruptions
            self.history["acc_exp_car_interruptions"][
                time
            ] = self.acc_exp_car_interruptions
            self.history["acc_interruption_duration"][
                time
            ] = self.acc_interruption_duration.get_hours()
            self.history["acc_available_num_cars"][
                time
            ] = self.acc_available_num_cars

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute

        Parameters
        ----------
        attribute : str
            System attribute

        Returns
        ----------
        history[attribute] : dict
            Returns the history variables of an attribute

        """
        return self.history[attribute]

    def update_fail_status(self, dt: Time):
        """
        Locks og unlocks the battery functionality based on failure states of the basestation

        Parameters
        ----------
        dt : Time
            The current time step

        Returns
        ----------
        None

        """
        pass

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

    def print_status(self):

        """
        Prints the status of the EV park

        Parameters
        ----------
        None

        Returns
        ----------
        None
        """

        print("EV park status")
        print("name: {}".format(self.name))
        print("parent bus: {}".format(self.bus.name))
        print("inj_p_max: {} MW".format(self.inj_p_max))
        print("inj_q_max: {} MVar".format(self.inj_q_max))
        print("E_max: {} MWh".format(self.E_max))
        print("SOC_min: {}".format(self.SOC_min))
        print("SOC_max: {}".format(self.SOC_max))
        print("SOC: {:.2f}".format(self.get_SOC))

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
        self.curr_p_demand = 0
        self.curr_q_demand = 0
        self.curr_p_charge = 0
        self.curr_q_charge = 0
        self.available_cars.clear()
        self.available_num_cars = 0
        ## Reliability attributes
        self.num_consecutive_interruptions = 0
        self.park_interruption_fraction = 0
        self.acc_available_num_cars = 0
        self.acc_num_interruptions = 0
        self.curr_exp_interruptions = 0
        self.acc_exp_interruptions = 0
        self.curr_exp_car_interruptions = 0
        self.acc_exp_car_interruptions = 0
        self.acc_interruption_duration = Time(0)
        self.curr_interruption_duration = Time(0)
        if save_flag:
            self.initialize_history()
