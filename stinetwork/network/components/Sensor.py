from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Line import Line
from stinetwork.utils import (
    random_choice,
    TimeUnit,
    Time,
    convert_yearly_fail_rate,
)


class SensorState(Enum):
    OK = 1
    FAILED = 2
    REPAIR = 3


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

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        line: Line,
        fail_rate_per_year: float = 0,
        p_repair_new_signal: float = 0,
        p_repair_reboot: float = 0,
        new_signal_time: Time = Time(0, TimeUnit.SECOND),
        reboot_time: Time = Time(2, TimeUnit.MINUTE),
        manual_repair_time: Time = Time(2, TimeUnit.HOUR),
        state: SensorState = SensorState.OK,
    ):

        self.name = name
        self.line = line
        line.sensor = self
        self.fail_rate_per_year = fail_rate_per_year
        self.p_repair_new_signal = p_repair_new_signal
        self.p_repair_reboot = p_repair_reboot
        self.new_signal_time = new_signal_time
        self.reboot_time = reboot_time
        self.manual_repair_time = manual_repair_time
        self.outage_time = 0
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

    def fail(self):
        self.state = SensorState.FAILED

    def not_fail(self):
        self.state = SensorState.OK

    def draw_fail_status(self, dt: Time):
        p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
        self.draw_status(p_fail)

    def draw_status(self, prob):
        if random_choice(self.ps_random, prob):
            self.fail()
        else:
            self.not_fail()

    def repair(self, dt: Time):
        repair_time = self.new_signal_time
        self.draw_status(dt, self.p_repair_new_signal)
        if self.state == SensorState.OK:
            return repair_time, self.line.failed
        elif self.state == SensorState.FAILED:
            repair_time += self.reboot_time
            self.draw_status(dt, self.p_repair_reboot)
            if self.state == SensorState.OK:
                return repair_time, self.line.failed
            elif self.state == SensorState.FAILED:
                self.remaining_repair_time = self.manual_repair_time
                self.state = SensorState.REPAIR
                return repair_time, True

    def get_line_fail_status(self, dt: Time):
        self.draw_fail_status(dt)
        if self.state == SensorState.OK:
            return 0, self.line.failed
        elif self.state == SensorState.FAILED:
            return self.repair(dt)
        elif self.state == SensorState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time.is_zero():
                self.not_fail()
            return None

    def get_line_connection_status(self, dt: Time):
        self.set_fail_status(dt)
        if self.state == SensorState.OK:
            return self.line.connected
        elif self.state == SensorState.FAILED:
            return None

    def get_section(self):
        return self.line.section

    def update_fail_status(self, dt: Time):
        pass

    def update_history(self, prev_time, curr_time, save_flag: bool):
        pass

    def get_history(self, attribute: str):
        pass

    def add_random_seed(self, random_gen):
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
        pass

    def reset_status(self, save_flag: bool):
        pass
