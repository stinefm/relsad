from .Component import Component
from .Bus import Bus
from .Battery import Battery
from .MicrogridController import MicrogridMode
import numpy as np
from relsad.Time import (
    Time,
    TimeUnit,
)
from relsad.StatDist import StatDist

"""
### What it should include: ### 

    1. Number of cars - The total amount of cars that can be charging at the same time
    2. Inverter capacity of the charger
    3. The efficiency of the charger
    4. The SOC level, the min SOC and the max SOC

    Each time a failure occurs the model will draw the amount of cars at the EV park and the SOC level of each car
    This will follow a uniform distribution (binomial distribution?)
    If V2G is applied - need a TRUE/FALSE variable that one can turn on and off based on if the system should
    include V2G or just only EV. 

    If only EV: 
        The EV park will be seen as a load and will charge the cars with power
    If V2G:
        The EV park will be seen as a battery if it is in an island mode with no other production
            if there is other production, this should be used first
            if there is more production than load, then the EV park can charge the cars instead. 
    
    Assumptions: 
        During a failure no new cars can come to the park and now cars will leave the park during the outage period. 
        Do not consider which time of the day the failure occurs
        Assume equal size of all cars
        


"""

class EVPark(Component):

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self, 
        name: str, 
        bus: Bus,
        num_ev_dist: StatDist,
        inj_p_max: float = 0.072,
        inj_q_max: float = 0.072,
        E_max: float = 0.75,
        SOC_min: float = 0.1, 
        SOC_max: float = 0.9, 
        n_battery: float = 0.95,
        v2g_flag: bool = True,
    ): 

        self.name = name

        self.bus = bus
        bus.ev_park = self

        self.num_ev_dist = num_ev_dist
        self.inj_p_max = inj_p_max
        self.inj_q_max = inj_q_max
        self.E_max = E_max
        self.SOC_min = SOC_min
        self.SOC_max = SOC_max
        self.n_battery = n_battery

        self.curr_demand = None
        self.curr_charge = None

        self.v2g_flag = v2g_flag

        self.cars = list()
        self.num_cars = None

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
        Draw the number of EVs in the park at that time and
        the SOC level of each car which will make the SOC level of the park 
        """
        self.num_cars = round(self.num_ev_dist.get(hour_of_day))
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
            )
            for i in range(self.num_cars)
            ]
        for i, car in enumerate(self.cars):
            car.E_battery = soc_states[i]*self.E_max
            car.update_SOC()

    def update(self, p, q, fail_duration: Time, dt: Time, hour_of_day: int):
        if fail_duration == dt:
            self.draw_current_state(hour_of_day)
        self.curr_demand = self.get_curr_demand(dt)
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
        pprod = max(0,p_change)
        qprod = max(0,q_change)
        pload = abs(min(0,p_change))
        qload = abs(min(0,q_change))
        self.curr_charge = pload - pprod
        return p, q

    def get_curr_demand(self, dt: Time):
        curr_demand = 0
        for car in self.cars:
            curr_demand += min(
                car.inj_p_max*dt.get_hours(),
                car.E_max*car.SOC_max - car.E_battery,
            )
        return curr_demand

    def get_SOC(self):
        if self.num_cars <= 0:
            return 0
        return np.mean([car.SOC for car in self.cars])

    def get_ev_index(self):
        return self.curr_demand - self.curr_charge

    def initialize_history(self):
        self.history["SOC"] = {}
        self.history["ev_index"] = {}
        self.history["demand"] = {}
        self.history["charge"] = {}
        self.history["num_cars"] = {}
        
    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        """
        Updates the history variables

        Parameters
        ----------
        curr_time : Time
            Current time

        Returns
        ----------
        None
        """
        if save_flag:
            self.history["SOC"][curr_time] = self.get_SOC()
            self.history["ev_index"][
                curr_time
            ] = self.get_ev_index()
            self.history["demand"][
                curr_time
            ] = self.curr_demand
            self.history["charge"][
                curr_time
            ] = self.curr_charge
            self.history["num_cars"][curr_time] = self.num_cars

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
        None

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
        None

        Returns
        ----------
        None

        """
        self.curr_demand = None
        self.curr_charge = None
        self.cars.clear()
        self.num_cars = None
        if save_flag:
            self.initialize_history()