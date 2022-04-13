import numpy as np
from .Component import Component
from .Bus import Bus
from relsad.Time import Time


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
    prod_dict : dict
        Dictionary over the production units
    pprod : float
        The active power produced by the production unit \[MW\]
    qprod : float
        The reactive power produced by the production unit \[MVar\]
    pmax : float
        The maximum active power that can be produced by the production unit \[MW\]
    qmax : float
        The maximum reactive power that can be produced by the production unit \[MVar\]
    history : dict
        Dictonary attribute that stores the historic variables


    Methods
    ----------
    add_prod_dict(prod_dict)
        Adds a production dictionary to the class
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
        self, name: str, bus: Bus, pmax: float = 10, qmax: float = 10
    ):

        """
        Constructs all the necessary attributes for the production object

        Parameters
        ----------
            name : string
                Name of the production unit
            bus : Bus
                The bus the production unit is connected to
            pprod : float
                The active power produced by the production unit [MW]
            qprod : float
                The reactive power produced by the production unit [MVar]
            pmax : float
                The maximum active power that can be produced by the production unit [MW]
            qmax : float
                The maximum reactive power that can be produced by the production unit [MVar]
        """
        self.name = name
        self.bus = bus
        bus.prod = self
        self.prod_dict = dict()
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

    def add_prod_dict(self, prod_dict: dict):
        """
        Adds a production dictionary to the class

        Parameters
        ----------
        prod_dict : dict
            Dictionary over the production

        Returns
        ----------
        None

        """
        self.prod_dict = prod_dict

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
        pprod = self.prod_dict["pprod"][inc_idx]
        qprod = self.prod_dict["qprod"][inc_idx]
        if pprod > self.pmax:
            self.pprod = self.pmax
        else:
            self.pprod = pprod
        if qprod > self.qmax:
            self.qprod = self.qmax
        else:
            self.qprod = qprod
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
