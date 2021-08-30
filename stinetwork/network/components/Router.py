from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Disconnector import Disconnector
from stinetwork.utils import random_choice


class RouterState(Enum):
    OK = 1
    FAILED = 2


class Router(Component):

    ## Visual attributes
    marker = "x"
    size = 2 ** 2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=1,
        markersize=size,
        linestyle="None",
    )
    color = "orange"

    def __init__(
        self,
        name: str,
        disconnector: Disconnector,
        fail_rate: float = 0,
        outage_time: float = 1,
        state: RouterState = RouterState.OK,
    ):

        self.name = name
        self.disconnector = disconnector
        disconnector.router = self
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Router(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Router)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def open_disconnector(self, curr_time):
        if self.state == RouterState.OK:
            self.disconnector.open()
        elif self.state == RouterState.FAILED:
            pass

    def close_disconnector(self, curr_time):
        if self.state == RouterState.OK:
            self.disconnector.close()
        elif self.state == RouterState.FAILED:
            pass

    def update_fail_status(self, curr_time):
        pass

    def update_history(self, curr_time, save_flag: bool):
        pass

    def get_history(self, attribute: str):
        pass

    def add_random_seed(self, random_gen):
        pass

    def print_status(self):
        pass

    def reset_status(self, save_flag: bool):
        pass