class CostFunction:
    """
    Class defining a cost function

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
