from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Line import Line
from stinetwork.utils import random_choice


class SensorState(Enum):
    OK = 1
    FAILED = 2


class Sensor(Component):

    ## Visual attributes
    marker = "s"
    size = 2 ** 2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=1,
        markersize=size,
        linestyle="None",
    )
    color = "red"

    def __init__(
        self,
        name: str,
        line: Line,
        fail_rate: float = 0,
        outage_time: float = 1,
        state: SensorState = SensorState.OK,
    ):

        self.name = name
        self.line = line
        line.sensor = self
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Sensor(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Sensor)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def get_line_fail_status(self):
        if self.state == SensorState.OK:
            return self.line.failed
        elif self.state == SensorState.FAILED:
            return None

    def get_line_connection_status(self):
        if self.state == SensorState.OK:
            return self.line.connected
        elif self.state == SensorState.FAILED:
            return None

    def get_section(self):
        return self.line.section

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
