import numpy as np

from relsad.Time import Time
from relsad.utils import interpolate

from .Bus import Bus
from .Component import Component


class Production(Component):

    """
    Common class for production

    ...

    Attributes
    ----------
    name : string
        Name of the production unit
    bus : Bus
        The bus the production unit is connected to
    pprod_data : np.ndarray
        Array of active production data
    qprod_data : np.ndarray
        Array of reactive production data
    pprod : float
        The active power produced by the production unit [MW]
    qprod : float
        The reactive power produced by the production unit [MVar]
    pmax : float
        The maximum active power that can be produced by the production unit [MW]
    qmax : float
        The maximum reactive power that can be produced by the production unit [MVar]
    history : dict
        Dictonary attribute that stores the historic variables


    Methods
    ----------
    add_prod_data(pprod_data, qprod_data)
        Adds production data to the production component
    prepare_prod_data(time_indices)
        Prepares the production data for the current time step configuration
    add_prod(pprod, qprod)
        Adds production to the bus
    set_prod(curr_time)
        Decides how much active and reactive power that will be produced
    update_bus_prod()
        Updates the production on the bus with the amount of generated active and reactive power
        Sets the active production at the bus equal the active production at the bus minus the generated active power
        Sets the reactive production at the bus equal the reactive production at the bus minus the generated reactive power
    reset_prod()
        Resets the active and reactive production
    update_fail_status()
        Updates the fail status
    update_history(curr_time)
        Updates the history variables
    get_history(attribute)
        Returns the history variables of an attribute
    add_random_instance(random_gen)
        Adds global random seed
    print_status()
        Prints the status
    reset_status()
        Resets and sets the status of the class parameters

    """

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        bus: Bus,
        pmax: float = 10,
        qmax: float = 10,
    ):

        # Verify input
        if bus is None:
            raise Exception("Production unit must be connected to a Bus")
        if bus.parent_network is not None:
            raise Exception(
                "Production unit must be created before the bus is connected to a network"
            )
        if pmax < 0:
            raise Exception(
                "The maximum active power that can be produced must be positive"
            )
        if qmax < 0:
            raise Exception(
                "The maximum reactive power that can be produced must be positive"
            )

        self.name = name
        self.bus = bus
        bus.prod = self
        self.pprod_data = None
        self.qprod_data = None
        self.pprod = 0
        self.qprod = 0
        self.pmax = pmax
        self.qmax = qmax

        ## History
        self.history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Production(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Production)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_prod_data(
        self,
        pprod_data: np.ndarray,
        qprod_data: np.ndarray = None,
    ):
        """
        Adds production data to the production component

        Parameters
        ----------
        pprod_data : np.ndarray
            Active power production array
        qprod_data : np.ndarray
            Reactive power production array

        Returns
        ----------
        None

        """
        self.pprod_data = pprod_data
        if qprod_data is None:
            self.qprod_data = np.zeros_like(pprod_data)
        else:
            self.qprod_data = qprod_data

    def prepare_prod_data(
        self,
        time_indices: np.ndarray,
    ):
        """
        Prepares the production data for the current time step configuration

        Parameters
        ----------
        time_indices : np.ndarray
            Time indices used to discretize the production data

        Returns
        ----------
        None

        """
        if self.pprod_data is None:
            raise Exception(
                "Active production data must be provided for {:s}".format(
                    self.name
                )
            )

        self.pprod_data = interpolate(
            array=self.pprod_data,
            time_indices=time_indices,
        )

        if self.qprod_data is None:
            raise Exception(
                "Reactive production data must be provided for {:s}".format(
                    self.name
                )
            )

        self.qprod_data = interpolate(
            array=self.qprod_data,
            time_indices=time_indices,
        )

    def add_prod(
        self,
        pprod: float,
        qprod: float,
    ):
        """
        Adds production to the bus

        Parameters
        ----------
        pprod : float
            Active power
        qprod : float
            Reactive power

        Returns
        ----------
        None

        """
        # MW and MVar
        self.pprod += pprod
        self.qprod += qprod

    def set_prod(self, inc_idx: int):
        """
        Decides how much active and reactive power that will be produced

        Parameters
        ----------
        inc_idx : int
            Index of current increment

        Returns
        ----------
        None

        """
        self.reset_prod()
        pprod = self.pprod_data[inc_idx]
        qprod = self.qprod_data[inc_idx]
        if pprod > self.pmax:
            pprod = self.pmax
        if qprod > self.qmax:
            qprod = self.qmax
        self.add_prod(pprod, qprod)
        self.update_bus_prod()

    def update_bus_prod(self):
        """
        Updates the production on the bus with the amount of generated active and reactive power
        Sets the active production at the bus equal the active production at the bus minus the generated active power
        Sets the reactive production at the bus equal the reactive production at the bus minus the generated reactive power

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.bus.pprod = self.pprod  # MW
        self.bus.qprod = self.qprod  # MVar
        self.bus.pprod_pu = self.pprod / self.bus.s_ref  # PU
        self.bus.qprod_pu = self.qprod / self.bus.s_ref  # PU

    def reset_prod(self):
        """
        Resets the active and reactive production

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        self.pprod = 0
        self.qprod = 0

    def update_fail_status(self, dt: Time):
        """
        Updates the fail status

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """

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
        Prints the status

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """

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
        self.history = {}


if __name__ == "__main__":
    pass
