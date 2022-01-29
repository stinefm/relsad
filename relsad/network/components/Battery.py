from .Component import Component
from .Bus import Bus
from .MicrogridController import MicrogridMode
import numpy as np
from relsad.utils import INF
from relsad.Time import (
    Time,
    TimeUnit,
)


class Battery(Component):
    """
    Common class for batteries

    ...

    Attributes
    ----------
    name : string
        Name of the battery
    mode : str
        Microgrid mode
    survival_time : Time
        Total amount of hours the microgrid should survive on battery capacity
    remaining_survival_time : Time
        The time left for the battery to ensure energy for the microgrid load
    standard_SOC_min : float
        The minimum State of Charge for the battery which can change based on wanted battery capacity
    bus : Bus
        The bus the battery is connected to
    inj_p_max : float
        The maximum active power that the battery can inject [MW]
    inj_q_max : float
        The maximum reactive power that the battery can inject [MVar]
    inj_max : float
        The maximum apperent power that the battery can inject [MVa]
    f_inj_p : float
    f_inj_q : float
    E_max : float
        The maximum capacity of the battery [MWh]
    SOC_min : float
        The minimal state of charge level in the battery
    SOC_max : float
        The maximum state of charge level in the battery
    n_battery : float
        The battery efficiency
    p_inj : float
        The injected active power in the battery [MW]
    q_inj : float
        The injected reactive power in the battery [MVar]
    SOC : float
        The state of charge of the battery
    E_battery : float
        The amount of energy stored in the battery [MWh]
    lock : bool
        Boolean variable that locks the battery if a basestation is failed, locks the functionality of the battery
    history : dict
        Dictonary attribute that stores the historic variables

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
    update_bus_load_and_prod(system_load_balance_p, system_load_balance_q)
        Updates the load and production on the bus based on the system load balance
    update_history(curr_time, dt, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    update_fail_status(curr_time)
        Locks and unlocks the battery functionality based on failure states of the basestation
    add_random_instance(random_gen)
        Adds global random seed
    reset_status()
        Resets and sets the status of the system parameters
    set_mode(mode)
        Sets the microgrid mode
    start_survival_time()
        Starts the timer for how long the battery should focus on supporting own load
    """

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        bus: Bus,
        inj_p_max: float = 0.5,
        inj_q_max: float = 0.5,
        E_max: float = 1,
        SOC_min: float = 0.1,
        SOC_max: float = 1,
        n_battery: float = 0.95,
        ev_flag: bool = False,
    ):

        """
        Constructs all the necessary attributes for the production object

        Parameters
        ----------
        name : string
            Name of the battery
        mode : str
            Microgrid mode
        survival_time : Time
            Total amount of hours the microgrid should survive on battery capacity
        remaining_survival_time : Time
            The time left for the battery to ensure energy for the microgrid load
        standard_SOC_min : float
            The minimum State of Charge for the battery which can change based on wanted battery capacity
        bus : Bus
            The bus the battery is connected to
        inj_p_max : float
            The maximum active power that the battery can inject [MW]
        inj_q_max : float
            The maximum reactive power that the battery can inject [MVar]
        inj_max : float
            The maximum apperent power that the battery can inject [MVa]
        f_inj_p : float
        f_inj_q : float
        E_max : float
            The maximum capacity of the battery [MWh]
        SOC_min : float
            The minimal state of charge level in the battery
        SOC_max : float
            The maximum state of charge level in the battery
        n_battery : float
            The battery efficiency
        p_inj : float
            The injected active power in the battery [MW]
        q_inj : float
            The injected reactive power in the battery [MVar]
        SOC : float
            The state of charge of the battery
        E_battery : float
            The amount of energy stored in the battery [MWh]
        lock : bool
            Boolean variable that locks the battery if a basestation is failed, locks the functionality of the battery
        history : dict
            Dictonary attribute that stores the historic variables


        """

        self.name = name

        self.mode = None
        self.survival_time = Time(4, TimeUnit.HOUR)
        self.remaining_survival_time = Time(0)
        self.standard_SOC_min = SOC_min

        self.bus = bus
        if ev_flag is not True:
            bus.battery = self

        self.inj_p_max = inj_p_max  # MW
        self.inj_q_max = inj_q_max  # MVar
        self.inj_max = self.inj_p_max
        self.f_inj_p = 1  # active capacity fraction
        self.f_inj_q = (
            self.inj_q_max / self.inj_max
        )  # reactive capacity fraction

        self.E_max = E_max  # MWh
        self.SOC_min = SOC_min
        self.E_min = E_max * SOC_min  # MWh
        self.SOC_max = SOC_max
        self.n_battery = n_battery

        self.p_inj = 0.0  # MW
        self.q_inj = 0.0  # MVar
        self.SOC = SOC_min
        self.E_battery = self.SOC * self.E_max  # MWh
        self.update_SOC()

        self.lock = False

        ## History
        self.history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Battery(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Battery)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def update_SOC(self):
        """
        Updates the SOC in the battery

        Paramters
        ----------
        None

        Returns
        ----------
        None

        """
        self.SOC = self.E_battery / self.E_max

    def charge(self, p_ch, dt: Time):

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
        if p_ch > self.inj_p_max * dt.get_hours():
            p_ch_remaining += p_ch - self.inj_p_max * dt.get_hours()
            if p_ch >= INF:
                p_ch = self.inj_p_max * dt.get_hours()
            else:
                p_ch -= p_ch_remaining
        dE = self.n_battery * p_ch
        E_tr = self.E_battery + dE
        SOC_tr = E_tr / self.E_max
        dSOC = dE / self.E_max
        if SOC_tr > self.SOC_max:
            f = 1 - (SOC_tr - self.SOC_max) / dSOC
            self.E_battery += f * dE
            p_ch_remaining += (1 - f) * p_ch
        else:
            self.E_battery += dE
            p_ch_remaining += 0
        self.update_SOC()
        return p_ch_remaining

    def discharge(self, p_dis, q_dis, dt: Time):

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

        if self.remaining_survival_time > Time(0):
            self.remaining_survival_time -= dt
            self.SOC_min = min(
                self.bus.parent_network.get_max_load()[0]
                * self.remaining_survival_time.get_hours()
                / self.E_max
                + self.standard_SOC_min,
                self.SOC_max,
            )
        else:
            self.SOC_min = self.standard_SOC_min

        p_dis_remaining = 0
        q_dis_remaining = 0
        if p_dis > self.inj_p_max * dt.get_hours():
            p_dis_remaining += p_dis - self.inj_p_max * dt.get_hours()
            p_dis -= p_dis_remaining
        if q_dis > self.inj_q_max * dt.get_hours():
            q_dis_remaining += q_dis - self.inj_q_max * dt.get_hours()
            q_dis -= q_dis_remaining
        if p_dis + q_dis > self.inj_max * dt.get_hours():
            f_p = p_dis / (p_dis + q_dis)  # active fraction
            f_q = 1 - f_p  # reactive fraction
            diff = p_dis + q_dis - self.inj_max * dt.get_hours()
            p_dis_remaining += diff * (1 - f_p)
            q_dis_remaining += diff * (1 - f_q)
            p_dis -= diff * (1 - f_p)
            q_dis -= diff * (1 - f_q)

        dE = 1 / self.n_battery * (p_dis + q_dis)
        E_tr = self.E_battery - dE
        SOC_tr = E_tr / self.E_max
        dSOC = dE / self.E_max
        if SOC_tr < self.SOC_min and dSOC > 0:
            f = 1 - (self.SOC_min - SOC_tr) / dSOC
            self.E_battery -= f * dE
            p_dis_remaining += (1 - f) * p_dis
            q_dis_remaining += (1 - f) * q_dis
        else:
            self.E_battery -= dE
        self.update_SOC()
        return p_dis_remaining, q_dis_remaining

    def print_status(self):

        """
        Prints the status of the battery

        Parameters
        ----------
        None

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
        print("Efficiency: {} %".format(self.n_battery * 100))
        print("SOC_min: {}".format(self.SOC_min))
        print("SOC_max: {}".format(self.SOC_max))
        print("SOC: {:.2f}".format(self.SOC))

    def update_bus_load_and_prod(
        self,
        system_load_balance_p: float,
        system_load_balance_q: float,
        dt: Time,
    ):
        """
        Updates the load and production on the bus based on the system load balance.
        If the balance is negative, there is a surplus of production, and the battery will charge.
        If the balance is positive, there is a shortage of production, and the battery will discharge.
        Returns the remaining surplus/shortage of power

        Parameters
        ----------
        system_load_balance_p : float
            Active system load balance
        system_load_balance_q : float
            Reactive system load balance

        Returns
        ----------
        p_rem : float
            Remaining surplus/shortage active power
        q_rem : float
            Remianing surplus/shortage reactive power
        """
        p, q = system_load_balance_p, system_load_balance_q

        if self.lock:  # Trafo has failed
            p_rem, q_rem = p, q
            return p_rem, q_rem

        pprod, qprod, pload, qload = 0, 0, 0, 0
        if p >= 0 and q >= 0:
            p_dis, q_dis = self.discharge(p, q, dt)
            pprod = p - p_dis
            qprod = q - q_dis
        if p < 0 and q >= 0:
            pload = -p - self.charge(-p, dt)
            qprod = q - self.discharge(0, q, dt)[1]
        if p >= 0 and q < 0:
            pprod = p - self.discharge(p, 0, dt)[0]
        if p < 0 and q < 0:
            pload = -p - self.charge(-p, dt)
        # if self.SOC >= self.SOC_min:
        self.bus.pprod += pprod  # MW
        self.bus.qprod += qprod  # MVar
        self.bus.pprod_pu += pprod / self.bus.s_ref  # PU
        self.bus.qprod_pu += qprod / self.bus.s_ref  # PU
        # if self.SOC <= self.SOC_max:
        self.bus.pload += pload  # MW
        self.bus.qload += qload  # MVar
        self.bus.pload_pu += pload / self.bus.s_ref  # PU
        self.bus.qload_pu += qload / self.bus.s_ref  # PU
        p_rem = p + pload - pprod
        q_rem = q + qload - qprod
        self.p_inj = pload - pprod
        self.q_inj = qload - qprod
        return p_rem, q_rem

    def initialize_history(self):
        self.history["SOC"] = {}
        self.history["SOC_min"] = {}
        self.history["remaining_survival_time"] = {}

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
            self.history["SOC"][curr_time] = self.SOC
            self.history["SOC_min"][curr_time] = self.SOC_min
            self.history["remaining_survival_time"][
                curr_time
            ] = self.remaining_survival_time.get_unit_quantity(curr_time.unit)

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
        if self.bus.trafo_failed:
            self.lock = True
        else:
            self.lock = False

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
        self.SOC = self.standard_SOC_min
        self.E_battery = self.SOC * self.E_max
        self.lock = False
        if save_flag:
            self.initialize_history()

    def set_mode(self, mode):
        """
        Sets the microgrid mode

        Parameters
        ----------
        mode : str
            The microgrid mode

        Returns
        ----------
        None

        """
        self.mode = mode

    def start_survival_time(self):
        """
        Starts the timer for how long the battery should focus on supporting own load

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.remaining_survival_time = self.survival_time

    def draw_SOC_state(self):
        """
        Draws the SOC state based on a uniform distribution
        """
        self.E_battery = self.ps_random.uniform(
            low=self.E_min,
            high=self.E_max,
        )
        self.update_SOC()

    def update(self, p, q, fail_duration: Time, dt: Time):
        if (
            self.mode in [MicrogridMode.SURVIVAL, MicrogridMode.FULL_SUPPORT]
            and fail_duration == dt
        ):
            self.draw_SOC_state()
        p, q = self.update_bus_load_and_prod(p, q, dt)
        return p, q


if __name__ == "__main__":
    pass
