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


class ControllerState(Enum):
    OK = 1
    SOFTWARE_FAIL = 2
    HARDWARE_FAIL = 3
    REPAIR = 4


class MainController(Component):
    def __init__(
        self,
        name: str,
        fail_rate_per_year_hardware: float = 0.2,
        fail_rate_per_year_software: float = 12,
        p_repair_new_signal: float = 0.95,
        p_repair_reboot: float = 0.9,
        new_signal_time: Time = Time(2, TimeUnit.SECOND),
        reboot_time: Time = Time(5, TimeUnit.MINUTE),
        manual_repair_time_software: Time = Time(0.3, TimeUnit.HOUR),
        manual_repair_time_hardware: Time = Time(2.5, TimeUnit.HOUR),
        state: ControllerState = ControllerState.OK,
        section_time: Time = Time(1, TimeUnit.HOUR),
    ):

        self.name = name
        self.fail_rate_per_year_hardware = fail_rate_per_year_hardware
        self.fail_rate_per_year_software = fail_rate_per_year_software
        self.p_repair_new_signal = p_repair_new_signal
        self.p_repair_reboot = p_repair_reboot
        self.reboot_time = reboot_time
        self.manual_repair_time_software = manual_repair_time_software
        self.manual_repair_time_hardware = manual_repair_time_hardware
        self.state = state
        self.section_time = section_time

        self.distribution_controllers = list()
        self.microgrid_controllers = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Controller(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, MainController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def add_distribution_controller(self, controller):
        self.distribution_controllers.append(controller)
        controller.section_time = self.section_time

    def add_microgrid_controller(self, controller):
        self.microgrid_controllers.append(controller)
        controller.section_time = self.section_time

    def run_control_loop(self, curr_time: Time, dt: Time):
        for controller in self.distribution_controllers:
            controller.run_control_loop(curr_time, dt)
        for controller in self.microgrid_controllers:
            controller.run_control_loop(curr_time, dt)

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
