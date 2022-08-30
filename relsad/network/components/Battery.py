from enum import Enum
from numbers import Number

import numpy as np

from relsad.Time import Time, TimeUnit
from relsad.utils import INF

from .Bus import Bus
from .Component import Component
from .MicrogridController import MicrogridMode


class BatteryType(Enum):
    """
    Battery type

    Attributes
    ----------
    REGULAR : int
        Regular battery type
    EV : int
        Electric vehicle battery type
    """

    REGULAR = 1
    EV = 2


class BatteryState(Enum):
    """
    Battery state

    Attributes
    ----------
    ACTIVE : int
        Battery is active
    INACTIVE : int
        Battery is inactive
    """

    ACTIVE = 1
    INACTIVE = 2


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
        Active power capacity fraction
    f_inj_q : float
        Reactive power capacity fraction
    E_max : float
        The maximum capacity of the battery [MWh]
    SOC_min : float
        The minimal state of charge level in the battery
    SOC_max : float
        The maximum state of charge level in the battery
    n_battery : float
        The battery efficiency
    SOC_start : float
        The iteration start value for the state of charge level in the battery
    p_inj : float
        The injected active power in the battery [MW]
    q_inj : float
        The injected reactive power in the battery [MVar]
    SOC : float
        The state of charge of the battery
    E_battery : float
        The amount of energy stored in the battery [MWh]
    battery_type : BatteryType
        The battery type
    state : BatteryState
        Battery state
    history : dict
        Dictonary attribute that stores the historic variables

    Methods
    ----------
    update_SOC()
        Updates the SOC in the battery
    charge(P_ch, dt)
        Charge the battery. Decides how much the battery can charge based on the desired charging power. Restricted by the amount of power that can be stored, the maximum power that can be injected, and the maximum state of charge of the battery. Updates the state of charge of the battery.
        Returns a float telling how much power the battery is not able to charge
    discharge(P_dis, q_dis, dt)
        Discharge the battery. Decides how much the battery can discharge based on the available energy in the battery. Limited by the state of charge, the maximum power that can be injected, and the wanted amount of power from the battery. Updates the state of charge of the battery.
        Returns a float telling how much power the battery is not able to discharge
    print_status()
        Prints the status of the battery
    update_bus_load_and_prod(system_load_balance_p, system_load_balance_q)
        Updates the load and production on the bus based on the system load balance.
        If the balance is negative, there is a surplus of production, and the battery will charge.
        If the balance is positive, there is a shortage of production, and the battery will discharge.
        Returns the remaining surplus/shortage of power
    initialize_history()
        Initializes the history variables
    update_history(prev_time, curr_time, dt, save_flag)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    update_fail_status(dt)
        Locks and unlocks the battery functionality based on failure states of the basestation
    add_random_instance(random_gen)
        Adds global random seed
    reset_status()
        Resets and sets the status of the system parameters
    set_mode(mode)
        Sets the microgrid mode
    start_survival_time()
        Starts the timer for how long the battery should focus on supporting own load
        Only for when a microgrid is added and follows a survival mode
    set_SOC_state()
        Sets the SOC state
    draw_SOC_state()
        Draws the SOC state based on a uniform distribution
    update(p, q, fail_duration, dt)
        Updates the battery status for the current time step

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
        battery_type: BatteryType = BatteryType.REGULAR,
        random_instance: np.random.Generator = None,
        SOC_start: float = None,
    ):

        # Verify input
        if bus is None:
            raise Exception("Battery must be connected to a Bus")
        if bus.parent_network is not None and random_instance is None:
            raise Exception(
                "Battery must be created before the bus is connected to a network"
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
        if (
            SOC_start is not None
            and not isinstance(SOC_start, Number)
            and (SOC_start < 0 or SOC_start > 1)
        ):
            raise Exception(
                "The SOC start value must be a number between 0 and 1"
            )

        self.name = name

        self.ps_random = random_instance

        self.mode = None
        self.survival_time = Time(4, TimeUnit.HOUR)
        self.remaining_survival_time = Time(0)
        self.standard_SOC_min = SOC_min

        self.bus = bus

        self.battery_type = battery_type

        if battery_type == BatteryType.REGULAR:
            # Link battery to parent bus
            bus.battery = self

        self.inj_p_max = inj_p_max  # MW
        self.inj_q_max = inj_q_max  # MVar
        self.inj_max = self.inj_p_max
        # active capacity fraction
        self.f_inj_p = 1
        # reactive capacity fraction
        self.f_inj_q = self.inj_q_max / self.inj_max

        self.E_max = E_max  # MWh
        self.SOC_min = SOC_min
        self.E_min = E_max * SOC_min  # MWh
        self.SOC_max = SOC_max
        self.n_battery = n_battery

        if SOC_start is None:
            self.set_SOC_state(SOC_state=SOC_min)
        else:
            self.set_SOC_state(SOC_state=SOC_start)
        self.SOC_start = SOC_start

        self.p_inj = 0.0  # MW
        self.q_inj = 0.0  # MVar

        self.state = BatteryState.ACTIVE

        ## History
        self.history = {}
        self.initialize_history()

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

        Parameters
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

        Decides how much the battery can charge based on the desired charging power. Restricted by the amount of power that can be stored, the maximum power that can be injected, and the maximum state of charge of the battery

        Updates the state of charge of the battery

        Returns a float telling how much power the battery is not able to charge


        Parameters
        ----------
        p_ch : float
            Desired amount of active power to charge the battery  [MW]
        dt : Time
            The current time step

        Returns
        ----------
        P_ch_remaining : float
            Amount of active power exceeding the charging capacity [MW]


        """

        p_ch_remaining = 0
        if p_ch > self.inj_p_max:
            p_ch_remaining += p_ch - self.inj_p_max
            if p_ch >= INF:
                # "Infinite" power source available
                p_ch = self.inj_p_max
            else:
                p_ch -= p_ch_remaining
        # Change in energy
        dE = self.n_battery * p_ch * dt.get_hours()  # MWh
        # Energy level, trial step
        E_tr = self.E_battery + dE
        SOC_tr = E_tr / self.E_max
        dSOC = dE / self.E_max
        if SOC_tr > self.SOC_max:
            # Correcting step
            #
            # Factor to scale the energy level
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

        Decides how much the battery can discharge based on the available energy in the battery. Limited by the state of charge, the maximum power that can be injected, and the wanted amount of power from the battery

        Updates the state of charge of the battery

        Returns a float telling how much power the battery is not able to discharge


        Parameters
        ----------
        p_dis : float
            Amount of wanted active power from the network [MW]
        q_dis : float
            Amount of wanted reactive power from the network [MVar]
        dt : Time
            The current time step

        Returns
        ----------
        p_dis_remaining : float
            Amount of wanted active power from the network exceeding battery discharging capacity [MW]
        q_dis_remaining : float
            Amount of wanted reactive power from the network exceeding battery discharging capacity [MVar]

        """

        if (
            self.remaining_survival_time > Time(0)
            and self.mode == MicrogridMode.SURVIVAL
        ):
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
        if p_dis > self.inj_p_max:
            p_dis_remaining += p_dis - self.inj_p_max
            p_dis -= p_dis_remaining
        if q_dis > self.inj_q_max:
            q_dis_remaining += q_dis - self.inj_q_max
            q_dis -= q_dis_remaining
        if p_dis + q_dis > self.inj_max:
            f_p = p_dis / (p_dis + q_dis)  # active fraction
            f_q = 1 - f_p  # reactive fraction
            diff = p_dis + q_dis - self.inj_max
            p_dis_remaining += diff * (1 - f_p)
            q_dis_remaining += diff * (1 - f_q)
            p_dis -= diff * (1 - f_p)
            q_dis -= diff * (1 - f_q)

        dE = 1 / self.n_battery * (p_dis + q_dis) * dt.get_hours()  # MWh/MVarh
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
            Active power system load balance in MW
        system_load_balance_q : float
            Reactive power system load balance in MW
        dt : Time
            The current time step

        Returns
        ----------
        p_rem : float
            Remaining surplus/shortage active power
        q_rem : float
            Remianing surplus/shortage reactive power
        """
        p, q = system_load_balance_p, system_load_balance_q

        if self.state == BatteryState.INACTIVE:  # Trafo has failed
            p_rem, q_rem = p, q
            return p_rem, q_rem

        pprod, qprod, pload, qload = 0, 0, 0, 0
        if p >= 0 and q >= 0:
            p_rem, q_rem = self.discharge(p, q, dt)
            pprod = p - p_rem
            qprod = q - q_rem
        if p < 0 and q >= 0:
            p_rem = self.charge(-p, dt)
            q_rem = self.discharge(0, q, dt)[1]
            pload = -p - p_rem
            qprod = q - q_rem
        if p >= 0 and q < 0:
            p_rem = self.discharge(p, 0, dt)[0]
            pprod = p - p_rem
        if p < 0 and q < 0:
            p_rem = self.charge(-p, dt)
            pload = -p - p_rem

        # Add production to bus
        self.bus.pprod += pprod  # MW
        self.bus.qprod += qprod  # MVar
        self.bus.pprod_pu += pprod / self.bus.s_ref  # PU
        self.bus.qprod_pu += qprod / self.bus.s_ref  # PU

        # Add load to bus
        self.bus.add_load(
            pload=pload,
            qload=qload,
        )

        # Battery power injection
        self.p_inj = pload - pprod
        self.q_inj = qload - qprod

        # Remaining power
        p_rem = p + pload - pprod
        q_rem = q + qload - qprod
        return p_rem, q_rem

    def initialize_history(self):
        """
        Initializes the storage of the history variables

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
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
        if save_flag:
            time = curr_time.get_unit_quantity(curr_time.unit)
            self.history["SOC"][time] = self.SOC
            self.history["SOC_min"][time] = self.SOC_min
            self.history["remaining_survival_time"][
                time
            ] = self.remaining_survival_time.get_unit_quantity(curr_time.unit)

    def get_history(self, attribute: str):
        """
        Returns the history variables of an attribute

        Parameters
        ----------
        attribute : str
            Battery attribute

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
        if self.bus.trafo_failed:
            self.state = BatteryState.INACTIVE
        else:
            self.state = BatteryState.ACTIVE

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
        save_flag : bool
            Indicates if saving is on or off

        Returns
        ----------
        None

        """
        if self.SOC_start is None:
            self.set_SOC_state(SOC_state=self.standard_SOC_min)
        else:
            self.set_SOC_state(SOC_state=self.SOC_start)
        self.state = BatteryState.ACTIVE
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
        Only for when a microgrid is added and follows a survival mode

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.remaining_survival_time = self.survival_time

    def set_SOC_state(self, SOC_state: float):
        """
        Sets the SOC state

        Parameters
        ----------
        SOC_state : float
            SOC value, between SOC_min and SOC_max

        Returns
        ----------
        None

        """
        if SOC_state < self.SOC_min or SOC_state > self.SOC_max:
            raise Exception("Not a valid SOC state")
        self.E_battery = SOC_state * self.E_max
        self.update_SOC()

    def draw_SOC_state(self):
        """
        Draws the SOC state based on a uniform distribution

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.E_battery = self.ps_random.uniform(
            low=self.E_min,
            high=self.E_max,
        )
        self.update_SOC()

    def update(self, p: float, q: float, fail_duration: Time, dt: Time):
        """
        Updates the battery status for the current time step

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

        Returns
        ----------
        p : float
            Remaining active power balance of the parent power system
        q : float
            Remaining reactive power balance of the parent power system
        """
        if (
            self.mode in [MicrogridMode.SURVIVAL, MicrogridMode.FULL_SUPPORT]
            and fail_duration == dt
        ):
            # Special handling for microgrid modes
            # Failure occurred in current time step
            self.draw_SOC_state()
        p, q = self.update_bus_load_and_prod(p, q, dt)
        return p, q


if __name__ == "__main__":
    pass
