class CostFunction:
    """
    Class defining a linear energy shedding
    cost function for a bus on the form

    cost = A + B * active_energy_shedded

    ...

    Attributes
    ----------
    A : float
        Constant cost factor parameter
    B : float
        Variable cost factor parameter



    Methods
    ----------
    """

    def __init__(
        self,
        A: float,
        B: float,
    ):
        self.A = A
        self.B = B
