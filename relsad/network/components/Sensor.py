from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Line import Line
from relsad.utils import (
    random_choice,
    convert_yearly_fail_rate,
)
from relsad.Time import (
    TimeUnit,
    Time,
)


class SensorState(Enum):
    OK = 1
    FAILED = 2
    REPAIR = 3


class Sensor(Component):

    ## Visual attributes
    color = "rosybrown"
    marker = "s"
    size = 2 ** 2
    handle = mlines.Line2D(
        [],
        [],
        marker=marker,
        markeredgewidth=1,
        markersize=size,
        color=color,
        linestyle="None",
    )

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        line: Line,
        fail_rate_per_year: float = 0.023,
        p_fail_repair_new_signal: float = 1 - 0.95,
        p_fail_repair_reboot: float = 1 - 0.9,
        new_signal_time: Time = Time(2, TimeUnit.SECOND),
        reboot_time: Time = Time(5, TimeUnit.MINUTE),
        manual_repair_time: Time = Time(2, TimeUnit.HOUR),
        state: SensorState = SensorState.OK,
    ):

        self.name = name
        self.line = line
        line.sensor = self
        self.fail_rate_per_year = fail_rate_per_year
        self.p_fail_repair_new_signal = p_fail_repair_new_signal
        self.p_fail_repair_reboot = p_fail_repair_reboot
        self.new_signal_time = new_signal_time
        self.reboot_time = reboot_time
        self.remaining_repair_time = Time(0)
        self.manual_repair_time = manual_repair_time
        self.state = state

        ## History
        self.history = {}
        self.monte_carlo_history = {}

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
        p_not_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
        self.draw_status(p_not_fail)

    def draw_status(self, prob):
        if random_choice(self.ps_random, prob):
            self.fail()
        else:
            self.not_fail()

    def repair(self, dt: Time):
        repair_time = self.new_signal_time
        self.draw_status(self.p_fail_repair_new_signal)
        if self.state == SensorState.OK:
            return repair_time, self.line.failed
        elif self.state == SensorState.FAILED:
            repair_time += self.reboot_time
            self.draw_status(self.p_fail_repair_reboot)
            if self.state == SensorState.OK:
                return repair_time, self.line.failed
            elif self.state == SensorState.FAILED:
                self.remaining_repair_time = self.manual_repair_time
                self.state = SensorState.REPAIR
                return repair_time, True

    def get_line_fail_status(self, dt: Time):
        if self.state == SensorState.REPAIR:
            return Time(0), True
        else:
            if self.state == SensorState.OK:
                return Time(0), self.line.failed
            elif self.state == SensorState.FAILED:
                return self.repair(dt)

    def get_section(self):
        return self.line.section

    def update_fail_status(self, dt: Time):
        if self.state == SensorState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time <= Time(0):
                self.not_fail()
        elif self.state == SensorState.OK:
            self.draw_fail_status(dt)

    def update_history(self, prev_time, curr_time, save_flag: bool):
        if save_flag:
            self.history["remaining_repair_time"][
                curr_time
            ] = self.remaining_repair_time.get_unit_quantity(curr_time.unit)
            self.history["state"][curr_time] = self.state.value

    def get_history(self, attribute: str):
        return self.history[attribute]

    def add_random_instance(self, random_gen):
        """
        Adds global random instance

        Parameters
        ----------
        random_gen : np.random.default_rng()
            Random number generator

        Returns
        ----------
        None

        """
        self.ps_random = random_gen

    def print_status(self):
        pass

    def reset_status(self, save_flag: bool):
        self.state = SensorState.OK
        self.remaining_repair_time = Time(0)
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        self.history["remaining_repair_time"] = {}
        self.history["state"] = {}
