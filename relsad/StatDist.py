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
    CUSTOM_DISCRETE = 4

UniformParameters = namedtuple("UniformParameters", ["min_val", "max_val"])
NormalParameters = namedtuple("NormalParameters", ["loc", "scale", "min_val", "max_val"])
CustomDiscreteParameters = namedtuple("CustomDiscreteParameters", ["xk", "pk"])


class StatDist:


    def __init__(
        self,
        stat_dist_type: StatDistType,
        parameters: namedtuple,
        draw_flag: bool=True,
        get_flag: bool=True,
    ):
        self.stat_dist_type = stat_dist_type
        self.parameters = parameters
        self.draw_flag = draw_flag
        self.get_flag = get_flag

    def draw(self, random_instance, size: int=1):
        if self.draw_flag is False:
            return None
        if self.stat_dist_type == StatDistType.UNIFORM_FLOAT:
            return random_instance.uniform(
                low=self.parameters.min_val,
                high=self.parameters.max_val,
                size=size,
            )
        elif self.stat_dist_type == StatDistType.UNIFORM_INT:
            return random_instance.integers(
                low=self.parameters.min_val,
                high=self.parameters.max_val,
                size=size,
            )
        elif self.stat_dist_type == StatDistType.TRUNCNORMAL:
            return stats.truncnorm.rvs(
                (self.parameters.min_val - self.parameters.loc) / self.parameters.scale,
                (self.parameters.max_val - self.parameters.loc) / self.parameters.scale,
                loc=self.parameters.loc,
                scale=self.parameters.scale,
                size=size,
                random_state=random_instance,
            )
        elif self.stat_dist_type == StatDistType.CUSTOM_DISCRETE:
            return stats.rv_discrete(
                values=(
                    self.parameters.xk,
                    self.parameters.pk,
                ),
                size=size,
                seed=random_instance,
            )

    def get(self, value):
        if self.get_flag is False:
            return None
        if self.stat_dist_type == StatDistType.CUSTOM_DISCRETE:
            return self.parameters.xk[value]

    def plot(self, path: str):
        n_points = 5000
        n_bins = 50
        rand_instance = random_instance()
        dist = self.draw(
            rand_instance,
            size=n_points,
        )
        fig, ax = plt.subplots()
        ax.hist(dist, bins=n_bins)
        fig.savefig(path)


if __name__=="__main__":
    stat_dist = StatDist(
        stat_dist_type=StatDistType.TRUNCNORMAL,
        parameters=NormalParameters(
            loc=1.25,
            scale=0.1,
            min_val=0.5,
            max_val=2,

        ),
        draw_flag=True,
        get_flag=False,
    )
    stat_dist.plot(path="stat_dist_plot.pdf")
