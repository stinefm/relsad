from .Component import Component
from .Bus import Bus


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
    pprod : float
        The active power produced by the production unit [MW]
    qprod : float
        The reactive power produced by the production unit [MVar]
    pmax : float
        The maximum active power that can be produced by the production unit [MW]
    qmax : float
        The maximum reactive power that can be produced by the production unit [MVar]


    Methods
    ----------
    set_prod(pprod, qprord)
        Decides how much active and reactive power that will be produced
    update_bus_load()
        Updates the load on the bus with the amount of generated active and reactive power

    """

    ## Random instance
    ps_random = None

    def __init__(self, name: str, bus: Bus, pmax: float = 1, qmax: float = 0):

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
        self.pprod = 0
        self.qprod = 0
        self.pmax = pmax
        self.qmax = qmax

        ## History
        self.history = dict()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Production(name={self.name})"

    def __eq__(self, other):
        try:
            return self.name == other.name
        except:
            False

    def __hash__(self):
        return hash(self.name)

    def set_prod(self, prod_dict: dict, curr_time):

        """
         Decides how much active and reactive power that will be produced
         If the produced power exceeds the maximal limit, the produced power is set to maximum limit
         The function updates the production on the bus by using the function update_bus_load()

         Parameters
         ----------
        prod_dict : dict
            A dictionary containing the production data for the production unit.
            The active power produced by the production unit [MW]
        curr_time : float

         Returns
         ----------
         None

        """
        day = curr_time // 24
        hour = curr_time % 24

        pprod = prod_dict["pprod"][day, hour]
        qprod = prod_dict["qprod"][day, hour]
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
        """
        self.bus.pprod = self.pprod
        self.bus.qprod = self.qprod

    def update_fail_status(self, curr_time):
        pass

    def update_history(self, curr_time):
        pass

    def get_history(self, attribute: str):
        return self.history[attribute]

    def add_random_seed(self, random_gen):
        """
        Adds global random seed
        """
        self.ps_random = random_gen

    def print_status(self):
        pass

    def reset_status(self):
        self.history = dict()


if __name__ == "__main__":
    pass
