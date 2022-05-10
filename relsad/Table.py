import numpy as np


class Table:

    """
    Utility class for tables in relsad

    ...

    Attributes
    ----------
    x : np.ndarray
        Table indices
    y : np.ndarray
        Table values


    Methods
    ----------
    get_value(value)
        Returns table value based on index

    """

    def __init__(
        self,
        x: np.ndarray,
        y: np.ndarray,
    ):
        # Check duplicate indices
        if len(np.unique(x)) != len(x):
            raise Exception("Tables indices are not unique")
        self.x = x
        self.y = y

    def get_value(self, index):
        """
        Returns table value based on index

        Parameters
        ----------
        index : int
            Table index

        Returns
        ----------
        value : float
            Table value based on index

        """
        if index not in self.x:
            raise Exception("Index {:d} not in table".format(index))
        value = self.y[self.x == index][0]
        return value
