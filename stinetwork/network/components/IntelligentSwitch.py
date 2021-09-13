from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .Disconnector import Disconnector
from stinetwork.utils import (
    random_choice,
    TimeUnit,
    Time,
    convert_yearly_fail_rate,
)


class IntelligentSwitchState(Enum):
    OK = 1
    FAILED = 2
    REPAIR = 3


class IntelligentSwitch(Component):

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

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        disconnector: Disconnector,
        fail_rate_per_year: float = 0.03,
        manual_repair_time: Time = Time(2, TimeUnit.HOUR),
        manual_section_time: Time = Time(1, TimeUnit.HOUR),
        state: IntelligentSwitchState = IntelligentSwitchState.OK,
    ):

        self.name = name
        self.disconnector = disconnector
        disconnector.intelligent_switch = self
        self.fail_rate_per_year = fail_rate_per_year
        self.remaining_repair_time = Time(0)
        self.manual_repair_time = manual_repair_time
        self.manual_section_time = manual_section_time
        self.state = state

        ## History
        self.history = {}
        self.monte_carlo_history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"IntelligentSwitch(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, IntelligentSwitch
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def fail(self):
        self.state = IntelligentSwitchState.FAILED

    def not_fail(self):
        self.state = IntelligentSwitchState.OK

    def draw_fail_status(self, dt: Time):
        p_fail = convert_yearly_fail_rate(self.fail_rate_per_year, dt)
        self.draw_status(p_fail)

    def draw_status(self, prob):
        if random_choice(self.ps_random, prob):
            self.fail()
        else:
            self.not_fail()

    def repair_open(self, dt: Time):
        self.remaining_repair_time = self.manual_repair_time
        self.state = IntelligentSwitchState.REPAIR
        return self.remaining_repair_time

    def open(self, dt: Time):
        if self.state == IntelligentSwitchState.REPAIR:
            return Time(0)
        else:
            self.draw_fail_status(dt)
            if self.state == IntelligentSwitchState.OK:
                self.disconnector.open()
                return Time(0)
            elif self.state == IntelligentSwitchState.FAILED:
                return self.repair_open(dt)

    def repair_close(self, dt: Time):
        self.remaining_repair_time = self.manual_repair_time
        self.state = IntelligentSwitchState.REPAIR

    def close(self, dt: Time):
        if not self.state == IntelligentSwitchState.REPAIR:
            self.draw_fail_status(dt)
            if self.state == IntelligentSwitchState.OK:
                self.disconnector.close()
            elif self.state == IntelligentSwitchState.FAILED:
                self.repair_close(dt)

    def update_fail_status(self, dt: Time):
        if self.state == IntelligentSwitchState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time <= Time(0):
                self.not_fail()

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
        self.remaining_repair_time = Time(0)
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        self.history["remaining_repair_time"] = {}
        self.history["state"] = {}
