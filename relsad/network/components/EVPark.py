from .Component import Component
from .Bus import Bus
from .Battery import Battery
from .MicrogridController import MicrogridMode
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)
from relsad.Table import Table


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
        Statistical distribution that gives the amount of EVs available at a given time in the network
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
    cars : list
        List of cars in the EV park
    num_cars : int
        Number of cars in the EV park
    num_consecutive_interruptions : int
        Number of consecutive interruptions an EV experiences
    interruption_fraction : float
        Fraction of interruptions on an EV
    acc_interruptions : float
        Accumulated interruptions an EV experiences
    curr_interruption_duration : Time
        Current interruption duration an EV experiences
    acc_interruption_duration : Time
        Accumulated interruption duration an EV experiences
    history : dict
        Dictonary attribute that stores the historic variables

    Methods
    ----------
    draw_current_state(hour_of_day)
        Draws the number of EVs in the park at that time and the SOC level of each EV which will make the SOC level of the EV park
    update(p, q, fail_duration, dt, hour_of_day)
        Updates the EV park status for the current time step
    get_curr_demand(dt)
        Gives the current power demand of an EV
    get_SOC()
        Gives the SOC level of the EV park
    get_ev_index()
        Gives the power demand of av EV that is not met by the system
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
            raise Exception(
                "EVPark must be connected to a Bus"
            )
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
            raise Exception(
                "The active power injection must be positive"
            )
        if inj_q_max < 0:
            raise Exception(
                "The reactive power injection must be positive"
            )
        if E_max < 0:
            raise Exception(
                "The energy capacity must be positive"
            )
        if SOC_min < 0 or SOC_max > 1:
            raise Exception(
                "The SOC limits must be between 0 and 1"
            )
        if n_battery < 0 or n_battery > 1:
            raise Exception(
                "The efficiency must be between 0 and 1"
            )

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

        self.cars = list()
        self.num_cars = 0

        ## Reliability attributes
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0
        self.curr_interruption_duration = Time(0)
        self.acc_interruption_duration = Time(0)

        ## History
        self.history = {}

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
        self.num_cars = round(self.num_ev_dist.get_value(hour_of_day))
        soc_states = self.ps_random.uniform(
            low=self.SOC_min,
            high=self.SOC_max,
            size=self.num_cars,
        )
        self.cars = [
            Battery(
                name="ev{:d}_{}".format(i, self.name),
                bus=self.bus,
                inj_p_max=self.inj_p_max,
                inj_q_max=self.inj_q_max,
                E_max=self.E_max,
                SOC_min=self.SOC_min,
                SOC_max=self.SOC_max,
                n_battery=self.n_battery,
                ev_flag=True,
                random_instance=self.ps_random,
            )
            for i in range(self.num_cars)
        ]
        for i, car in enumerate(self.cars):
            car.E_battery = soc_states[i] * self.E_max
            car.update_SOC()

    def update(self, p, q, fail_duration: Time, dt: Time, hour_of_day: int):
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
        (
            self.curr_p_demand,
            self.curr_q_demand,
        ) = self.get_curr_demand(dt)
        p_start = p
        q_start = q
        for car in self.cars:
            if self.v2g_flag is True:
                p, q = car.update_bus_load_and_prod(p, q, dt)
            else:
                if p < 0:
                    p, q = car.update_bus_load_and_prod(p, q, dt)
        p_change = p_start - p
        q_change = q_start - q
        pprod = max(0, p_change)
        qprod = max(0, q_change)
        pload = abs(min(0, p_change))
        qload = abs(min(0, q_change))
        self.curr_p_charge = pload - pprod
        self.curr_q_charge = qload - qprod
        return p, q

    def get_curr_demand(self, dt: Time):
        """
        Gives the current power demand of an EV

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
        for car in self.cars:
            curr_p_demand += min(
                car.inj_p_max,
                (car.E_max * car.SOC_max - car.E_battery) / dt.get_hours(),
            )
        return curr_p_demand, curr_q_demand

    def get_SOC(self):
        """
        Gives the SOC level of the EV park

        Parameters
        ----------
        None

        Returns
        ----------
        mean_SOC: float
            The average SOC value of the EV park

        """

        if self.num_cars <= 0:
            return 0
        mean_SOC = np.mean([car.SOC for car in self.cars])
        return mean_SOC

    def get_ev_index(self):
        """
        Gives the power demand of an EV that is not met by the system

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
        self.history["interruption_fraction"] = {}
        self.history["acc_interruptions"] = {}
        self.history["acc_interruption_duration"] = {}

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
        self.interruption_fraction = (
            abs(self.curr_p_charge / (self.inj_p_max * self.num_cars))
            if self.curr_p_charge < 0
            else 0
        )

        if self.interruption_fraction > 0:
            self.curr_interruptions += self.interruption_fraction
            self.num_consecutive_interruptions += 1
            self.curr_interruption_duration += dt
        else:
            if self.num_consecutive_interruptions >= 1:
                self.acc_interruptions += (
                    self.curr_interruptions
                    / self.num_consecutive_interruptions
                )
                self.acc_interruption_duration += (
                    self.curr_interruption_duration
                )
            self.curr_interruptions = 0
            self.curr_interruption_duration = Time(0)
            self.num_consecutive_interruptions = 0
        if save_flag:
            self.history["SOC"][curr_time] = self.get_SOC()
            self.history["ev_index"][curr_time] = self.get_ev_index()
            self.history["demand"][curr_time] = self.curr_p_demand
            self.history["charge"][curr_time] = self.curr_p_charge
            self.history["num_cars"][curr_time] = self.num_cars
            self.history["interruption_fraction"][
                curr_time
            ] = self.interruption_fraction
            self.history["acc_interruptions"][
                curr_time
            ] = self.acc_interruptions
            self.history["acc_interruption_duration"][
                curr_time
            ] = self.acc_interruption_duration

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
        self.cars.clear()
        self.num_cars = 0
        ## Reliability attributes
        self.num_consecutive_interruptions = 0
        self.interruption_fraction = 0
        self.curr_interruptions = 0
        self.acc_interruptions = 0
        self.acc_interruption_duration = Time(0)
        self.curr_interruption_duration = Time(0)
        if save_flag:
            self.initialize_history()
