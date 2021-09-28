from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .MainController import ControllerState
from relsad.network.containers import SectionState
from relsad.utils import (
    random_choice,
    Time,
    TimeUnit,
    convert_yearly_fail_rate,
    unique,
)


class DistributionController(Component):
    def __init__(
        self,
        name: str,
        network,
        fail_rate: float = 0,
        outage_time: Time = Time(1, TimeUnit.HOUR),
        state: ControllerState = ControllerState.OK,
    ):

        self.name = name
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state
        self.section_time = Time(0)
        self.check_components = False

        self.manual_section_time = None

        self.parent_controller = None

        self.network = network

        self.sensors = []

        self.failed_sections = []

        ## History
        self.history = {}
        self.monte_carlo_history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"DistributionController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, DistributionController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def check_circuitbreaker(self, curr_time: Time, dt: Time):
        if self.network.connected_line.circuitbreaker.is_open:
            if (
                self.section_time <= Time(0)
                and not self.network.connected_line.failed
            ):
                self.disconnect_failed_sections()
                self.network.connected_line.circuitbreaker.close()
                self.failed_sections = []

    def disconnect_failed_sections(self):
        for section in self.failed_sections:
            section.disconnect()

    def check_sensors(self, curr_time: Time, dt: Time):
        connected_sections = [
            x
            for x in self.network.sections
            if x.state == SectionState.CONNECTED
        ]
        disconnected_sections = [
            x
            for x in self.network.sections
            if x.state == SectionState.DISCONNECTED
        ]
        for section in disconnected_sections:
            sensors = unique([x.line.sensor for x in section.disconnectors])
            num_fails = 0
            for sensor in sensors:
                repair_time, line_fail_status = sensor.get_line_fail_status(dt)
                self.section_time += repair_time
                num_fails += 1 if line_fail_status else 0
            if num_fails == 0:
                section.connect(dt)
        for section in connected_sections:
            sensors = unique([x.line.sensor for x in section.disconnectors])
            num_fails = 0
            for sensor in sensors:
                repair_time, line_fail_status = sensor.get_line_fail_status(dt)
                self.section_time += repair_time
                num_fails += 1 if line_fail_status else 0
            if num_fails > 0:
                section.state = SectionState.FAILED
                self.section_time += section.get_disconnect_time(dt)
                self.failed_sections.append(section)
                self.failed_sections = unique(self.failed_sections)

    def run_control_loop(self, curr_time: Time, dt: Time):
        self.section_time = (
            self.section_time - dt if self.section_time > Time(0) else Time(0)
        )
        if (
            self.network.connected_line.circuitbreaker.is_open
            and self.section_time <= Time(0)
        ):
            self.check_components = True
        if self.check_components:
            self.check_sensors(curr_time, dt)
            self.spread_section_time_to_children()
            self.check_components = False
        self.check_circuitbreaker(curr_time, dt)

    def check_lines_manually(self, curr_time):
        connected_sections = [
            x
            for x in self.network.sections
            if x.state == SectionState.CONNECTED
        ]
        disconnected_sections = [
            x
            for x in self.network.sections
            if x.state == SectionState.DISCONNECTED
        ]
        for section in disconnected_sections:
            if sum([x.failed for x in section.lines]) == 0:
                section.connect_manually()
        for section in connected_sections:
            if sum([x.failed for x in section.lines]) > 0:
                section.state = SectionState.FAILED
                self.failed_sections.append(section)
                self.failed_sections = unique(self.failed_sections)
                self.section_time = self.manual_section_time
                for line in section.lines:
                    line.remaining_outage_time += self.section_time

    def run_manual_control_loop(self, curr_time: Time, dt: Time):
        self.section_time = (
            self.section_time - dt if self.section_time > Time(0) else Time(0)
        )
        if (
            self.network.connected_line.circuitbreaker.is_open
            and self.section_time <= Time(0)
        ):
            self.check_components = True
        if self.check_components:
            self.check_lines_manually(curr_time)
            self.spread_section_time_to_children()
            self.check_components = False
        self.check_circuitbreaker(curr_time, dt)

    def set_section_time(self, section_time):
        self.section_time = max(
            self.section_time,
            section_time,
        )

    def spread_section_time_to_children(self):
        for child_network in self.network.child_network_list:
            if (
                child_network.controller.network.connected_line.circuitbreaker.is_open
            ):
                child_network.controller.set_parent_section_time(
                    self.section_time
                )

    def update_fail_status(self, dt: Time):
        pass

    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        if save_flag:
            self.history["section_time"][
                curr_time
            ] = self.section_time.get_unit_quantity(curr_time.unit)

    def get_history(self, attribute: str):
        return self.history[attribute]

    def add_random_instance(self, random_gen):
        pass

    def print_status(self):
        pass

    def reset_status(self, save_flag: bool):
        self.section_time = Time(0)
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        self.history["section_time"] = {}