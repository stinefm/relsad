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

    ## Random instance
    ps_random: np.random.Generator = None

    def __init__(
        self,
        name: str,
        hardware_fail_rate_per_year: float = 0.2,
        software_fail_rate_per_year: float = 12,
        p_fail_repair_new_signal: float = 1 - 0.95,
        p_fail_repair_reboot: float = 0.9,
        new_signal_time: Time = Time(2, TimeUnit.SECOND),
        reboot_time: Time = Time(5, TimeUnit.MINUTE),
        manual_software_repair_time: Time = Time(0.3, TimeUnit.HOUR),
        manual_hardware_repair_time: Time = Time(2.5, TimeUnit.HOUR),
        manual_section_time: Time = Time(1, TimeUnit.HOUR),
        state: ControllerState = ControllerState.OK,
    ):

        self.name = name
        self.hardware_fail_rate_per_year = hardware_fail_rate_per_year
        self.software_fail_rate_per_year = software_fail_rate_per_year
        self.p_fail_repair_new_signal = p_fail_repair_new_signal
        self.p_fail_repair_reboot = p_fail_repair_reboot
        self.new_signal_time = new_signal_time
        self.reboot_time = reboot_time
        self.remaining_repair_time = Time(0)
        self.manual_software_repair_time = manual_software_repair_time
        self.manual_hardware_repair_time = manual_hardware_repair_time
        self.state = state
        self.section_time = Time(0)
        self.manual_section_time = manual_section_time

        self.distribution_controllers = list()
        self.microgrid_controllers = list()

        ## History
        self.history = {}
        self.monte_carlo_history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"MainController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, MainController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def fail_software(self):
        self.state = ControllerState.SOFTWARE_FAIL

    def fail_hardware(self):
        self.state = ControllerState.HARDWARE_FAIL

    def not_fail(self):
        self.state = ControllerState.OK

    def draw_fail_status(self, dt: Time):
        p_hardware_fail = convert_yearly_fail_rate(
            self.hardware_fail_rate_per_year, dt
        )
        self.draw_hardware_status(p_hardware_fail)
        if self.state == ControllerState.OK:
            p_software_fail = convert_yearly_fail_rate(
                self.software_fail_rate_per_year, dt
            )
            self.draw_software_status(p_software_fail)

    def draw_hardware_status(self, prob):
        if random_choice(self.ps_random, prob):
            self.fail_hardware()
        else:
            self.not_fail()

    def draw_software_status(self, prob):
        if random_choice(self.ps_random, prob):
            self.fail_software()
        else:
            self.not_fail()

    def repair_software_fail(self, dt: Time):
        repair_time = self.new_signal_time
        self.draw_software_status(self.p_fail_repair_new_signal)
        if self.state == ControllerState.OK:
            return repair_time
        elif self.state == ControllerState.SOFTWARE_FAIL:
            repair_time += self.reboot_time
            self.draw_software_status(self.p_fail_repair_reboot)
            if self.state == ControllerState.SOFTWARE_FAIL:
                self.remaining_repair_time = self.manual_software_repair_time
                self.state = ControllerState.REPAIR
            return repair_time

    def update_fail_status(self, dt: Time):
        if self.state == ControllerState.REPAIR:
            self.remaining_repair_time -= dt
            if self.remaining_repair_time <= Time(0):
                self.not_fail()
        elif self.state == ControllerState.OK:
            self.draw_fail_status(dt)
            if self.state == ControllerState.HARDWARE_FAIL:
                self.remaining_repair_time = self.manual_hardware_repair_time
                self.state == ControllerState.REPAIR
            elif self.state == ControllerState.SOFTWARE_FAIL:
                self.section_time = self.repair_software_fail(dt)
                self.spread_section_time_to_sub_controllers()

    def add_distribution_controller(self, controller):
        self.distribution_controllers.append(controller)
        controller.manual_section_time = self.manual_section_time

    def add_microgrid_controller(self, controller):
        self.microgrid_controllers.append(controller)
        controller.manual_section_time = self.manual_section_time

    def run_control_loop(self, curr_time: Time, dt: Time):
        if self.state == ControllerState.OK:
            for controller in self.distribution_controllers:
                controller.run_control_loop(curr_time, dt)
            for controller in self.microgrid_controllers:
                controller.run_control_loop(curr_time, dt)
        elif self.state == ControllerState.REPAIR:
            for controller in self.distribution_controllers:
                controller.run_manual_control_loop(curr_time, dt)
            for controller in self.microgrid_controllers:
                controller.run_manual_control_loop(curr_time, dt)

    def spread_section_time_to_sub_controllers(self):
        for controller in self.distribution_controllers:
            if controller.network.connected_line.circuitbreaker.is_open:
                controller.set_section_time(self.section_time)
        for controller in self.microgrid_controllers:
            if controller.network.connected_line.circuitbreaker.is_open:
                controller.set_section_time(self.section_time)

    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        if save_flag:
            self.history["section_time"][
                curr_time
            ] = self.section_time.get_unit_quantity(curr_time.unit)
            self.history["remaining_repair_time"][
                curr_time
            ] = self.remaining_repair_time.get_unit_quantity(curr_time.unit)
            self.history["state"][curr_time] = self.state.value

    def get_history(self, attribute: str):
        return self.history[attribute]

    def add_random_instance(self, random_gen):
        self.ps_random = random_gen

    def print_status(self):
        pass

    def reset_status(self, save_flag: bool):
        self.state = ControllerState.OK
        self.section_time = Time(0)
        self.remaining_repair_time = Time(0)
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        self.history["section_time"] = {}
        self.history["remaining_repair_time"] = {}
        self.history["state"] = {}
