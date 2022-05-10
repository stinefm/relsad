from enum import Enum
from collections import namedtuple
from scipy import stats
import numpy as np
import matplotlib.pyplot as plt
from relsad.utils import random_instance


class StatDistType(Enum):
    UNIFORM_FLOAT = 1
    UNIFORM_INT = 2
    TRUNCNORMAL = 3


UniformParameters = namedtuple("UniformParameters", ["min_val", "max_val"])
NormalParameters = namedtuple(
    "NormalParameters", ["loc", "scale", "min_val", "max_val"]
)


class StatDist:

    """
    Utility class for statistical distributions in relsad

    ...

    Attributes
    ----------
    stat_dist_type : StatDistType
        Type of statistical distribution
    parameters : namedtuple
        Statistical distribution parameters
    draw_flag : bool
        Flag indicating if drawing is allowed
    get_flag : bool


    Methods
    ----------
    draw(random_instance, size)
        Returns array of drawn instances of the statistical distribution
        of given size
    get_pdf(x)
        Returns the probability distribution function of
        the statistical distribution
    histplot(ax, n_points, n_bins)
        Plots the statistical distribution in a histogram
    plot(ax, x, color)

    """

    def __init__(
        self,
        stat_dist_type: StatDistType,
        parameters: namedtuple,
        draw_flag: bool = True,
        get_flag: bool = True,
    ):
        self.stat_dist_type = stat_dist_type
        self.parameters = parameters
        self.draw_flag = draw_flag
        self.get_flag = get_flag

    def draw(self, random_instance, size: int = 1):
        """
        Returns array of drawn instances of the statistical distribution
        of given size

        Parameters
        ----------
        random_instance : np.random.Generator
            Instance of a random generator
        size : int
            Size of drawn values

        Returns
        ----------
        drawn_values : np.ndarray
            Array of drawn instances of the statistical distribution
            of given size

        """
        drawn_values = None
        if self.draw_flag is False:
            return drawn_values
        if self.stat_dist_type == StatDistType.UNIFORM_FLOAT:
            drawn_values = random_instance.uniform(
                low=self.parameters.min_val,
                high=self.parameters.max_val,
                size=size,
            )
        elif self.stat_dist_type == StatDistType.UNIFORM_INT:
            drawn_values = random_instance.integers(
                low=self.parameters.min_val,
                high=self.parameters.max_val,
                size=size,
            )
        elif self.stat_dist_type == StatDistType.TRUNCNORMAL:
            drawn_values = stats.truncnorm.rvs(
                (self.parameters.min_val - self.parameters.loc)
                / self.parameters.scale,
                (self.parameters.max_val - self.parameters.loc)
                / self.parameters.scale,
                loc=self.parameters.loc,
                scale=self.parameters.scale,
                size=size,
                random_state=random_instance,
            )
        return drawn_values

    def get_pdf(
        self,
        x,
    ):
        """
        Returns the probability distribution function of
        the statistical distribution

        Parameters
        ----------
        x : np.ndarray
            Array of possible distribution values

        Returns
        ----------
        None

        """
        if self.stat_dist_type == StatDistType.UNIFORM_FLOAT:
            pass
        elif self.stat_dist_type == StatDistType.UNIFORM_INT:
            pass
        elif self.stat_dist_type == StatDistType.TRUNCNORMAL:
            return stats.truncnorm.pdf(
                x,
                (self.parameters.min_val - self.parameters.loc)
                / self.parameters.scale,
                (self.parameters.max_val - self.parameters.loc)
                / self.parameters.scale,
                loc=self.parameters.loc,
                scale=self.parameters.scale,
            )

    def histplot(
        self,
        ax,
        path: str,
        n_points: int = 5000,
        n_bins: int = 50,
    ):
        """
        Plots the statistical distribution in a histogram

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Plot axis
        path : str
            Save path
        n_points : int
            Number of distribution points
        n_bins : int
            Number of bins in histogram

        Returns
        ----------
        None

        """
        rand_instance = random_instance()
        dist = self.draw(
            rand_instance,
            size=n_points,
        )
        ax.hist(dist, bins=n_bins)
        fig.savefig(path)

    def plot(
        self,
        ax,
        x,
        color: str = "b",
    ):
        """
        Plots the statistical distribution in the provided axis

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Plot axis
        x : np.ndarray
            Array of possible distribution values
        color : str

        Returns
        ----------
        None

        """
        if self.stat_dist_type == StatDistType.UNIFORM_FLOAT:
            pass
        elif self.stat_dist_type == StatDistType.UNIFORM_INT:
            pass
        elif self.stat_dist_type == StatDistType.TRUNCNORMAL:
            ax.plot(
                x,
                stats.truncnorm.pdf(
                    x,
                    (self.parameters.min_val - self.parameters.loc)
                    / self.parameters.scale,
                    (self.parameters.max_val - self.parameters.loc)
                    / self.parameters.scale,
                    loc=self.parameters.loc,
                    scale=self.parameters.scale,
                ),
                color=color,
            )


if __name__ == "__main__":
    loc = 1.25
    scale = 0.1
    min_val, max_val = 0.5, 2
    stat_dist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=loc,
            scale=scale,
            min_val=min_val,
            max_val=max_val,
        ),
        draw_flag=True,
        get_flag=False,
    )
    fig, ax = plt.subplots()
    x = np.linspace(min_val, max_val, 1000)
    stat_dist.plot(ax=ax, x=x)
    fig.savefig(fname="stat_dist_plot.pdf")
