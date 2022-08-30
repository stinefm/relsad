from collections import namedtuple
from enum import Enum

import matplotlib.pyplot as plt
import numpy as np
import scipy.special as sps
from scipy import stats

from relsad.utils import get_random_instance


class StatDistType(Enum):
    """
    Statistical distribution type

    Attributes
    ----------
    UNIFORM_FLOAT : int
        Uniform distribution with floating point numbers.
        Parameters from UniformParameters:
        (min_val, max_val)
    UNIFORM_INT : int
        Uniform distribution with integers.
        Parameters from UniformParameters:
        (min_val, max_val)
    TRUNCNORMAL : int
        Truncated normal distribution.
        Parameters from NormalParameters:
        (loc, scale, min_val, max_val)
    GAMMA : int
        Gamma distribution
        Parameters from GammaParameters:
        (shape, scale)
    """

    UNIFORM_FLOAT = 1
    UNIFORM_INT = 2
    TRUNCNORMAL = 3
    GAMMA = 4


UniformParameters = namedtuple(
    "UniformParameters",
    ["min_val", "max_val"],
)
NormalParameters = namedtuple(
    "NormalParameters",
    ["loc", "scale", "min_val", "max_val"],
)
GammaParameters = namedtuple(
    "GammaParameters",
    ["shape", "scale"],
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
    ):
        self.stat_dist_type = stat_dist_type
        self.parameters = parameters

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
        if random_instance is None:
            random_instance = np.random.default_rng()
        drawn_values = None
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
        elif self.stat_dist_type == StatDistType.GAMMA:
            drawn_values = random_instance.gamma(
                shape=self.parameters.shape,
                scale=self.parameters.scale,
                size=size,
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
        elif self.stat_dist_type == StatDistType.GAMMA:
            return x ** (self.parameters.shape - 1) * (
                np.exp(-x / self.parameters.scale)
                / (
                    sps.gamma(self.parameters.shape)
                    * self.parameters.scale**self.parameters.shape
                )
            )

    def histplot(
        self,
        ax,
        n_points: int = 5000,
        n_bins: int = 50,
    ):
        """
        Plots the statistical distribution in a normalized histogram

        Parameters
        ----------
        ax : matplotlib.axes.Axes
            Plot axis
        n_points : int
            Number of distribution points
        n_bins : int
            Number of bins in histogram

        Returns
        ----------
        None

        """
        random_instance = get_random_instance()
        dist = self.draw(
            random_instance,
            size=n_points,
        )
        ax.hist(dist, bins=n_bins, density=True)

    def plot(
        self,
        ax,
        x,
        color: str = "b",
        label: str = None,
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
                self.get_pdf(x),
                color=color,
                label=label,
            )
        elif self.stat_dist_type == StatDistType.GAMMA:
            ax.plot(
                x,
                self.get_pdf(x),
                color=color,
                label=label,
            )


if __name__ == "__main__":
    trunc_normal_loc = 2
    trunc_normal_scale = 1
    min_val, max_val = 0, 20
    trunc_normal = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=trunc_normal_loc,
            scale=trunc_normal_scale,
            min_val=min_val,
            max_val=max_val,
        ),
    )

    gamma_1_shape = 1
    gamma_1_scale = 2
    gamma_1 = StatDist(
        stat_dist_type=StatDistType.GAMMA,
        parameters=GammaParameters(
            shape=gamma_1_shape,
            scale=gamma_1_scale,
        ),
    )

    gamma_2_shape = 7.5
    gamma_2_scale = 1
    gamma_2 = StatDist(
        stat_dist_type=StatDistType.GAMMA,
        parameters=GammaParameters(
            shape=gamma_2_shape,
            scale=gamma_2_scale,
        ),
    )
    fig, ax = plt.subplots()
    x = np.linspace(min_val, max_val, 1000)
    trunc_normal.plot(ax=ax, x=x)
    gamma_1.plot(ax=ax, x=x)
    gamma_1.histplot(ax=ax)
    gamma_2.plot(ax=ax, x=x)
    gamma_2.histplot(ax=ax)
    fig.savefig(fname="stat_dist_plot.pdf")
    plt.show()
