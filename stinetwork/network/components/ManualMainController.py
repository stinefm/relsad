from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from stinetwork.utils import (
    random_choice,
    Time,
    TimeUnit,
    convert_yearly_fail_rate,
)


class ManualMainController(Component):
    def __init__(
        self,
        name: str,
        section_time: Time,
    ):

        self.name = name
        self.section_time = section_time
        self.power_system = None

        self.distribution_controllers = list()
        self.microgrid_controllers = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ManualMainController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, ManualMainController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_distribution_controller(self, controller):
        self.distribution_controllers.append(controller)
        controller.manual_section_time = self.section_time

    def add_microgrid_controller(self, controller):
        self.microgrid_controllers.append(controller)
        controller.manual_section_time = self.section_time

    def run_control_loop(self, curr_time: Time, dt: Time):
        for controller in self.distribution_controllers:
            controller.run_manual_control_loop(curr_time, dt)
        for controller in self.microgrid_controllers:
            controller.run_manual_control_loop(curr_time, dt)

    def update_fail_status(self, dt: Time):
        pass

    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        pass

    def get_history(self, attribute: str):
        pass

    def add_random_instance(self, random_gen):
        pass

    def print_status(self):
        pass

    def reset_status(self, save_flag: bool):
        pass

    def initialize_history(self):
        pass
