from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .MainController import ControllerState
from stinetwork.utils import random_choice


class MicrogridController(Component):
    def __init__(
        self,
        name: str,
        network,
        fail_rate: float = 0,
        outage_time: float = 1,
        state: ControllerState = ControllerState.OK,
    ):

        self.name = name
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state
        self.section_time = None
        self.prev_section_time = 0
        self.remaining_section_time = 0

        self.network = network

        self.sensors = list()

        ## History
        self.history = {}
        self.monte_carlo_history = {}

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Controller(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, MicrogridController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def check_circuitbreaker(self, curr_time):
        if (
            self.network.connected_line.circuitbreaker.is_open
            and self.remaining_section_time == 0
        ):
            self.remaining_section_time = self.section_time
            self.prev_section_time = curr_time
        elif (
            self.network.connected_line.circuitbreaker.is_open
            and curr_time > self.prev_section_time
        ):
            if self.remaining_section_time >= 1:
                self.remaining_section_time -= 1
            if (
                self.remaining_section_time == 0
                and not self.network.connected_line.failed
            ):
                # If circuitbreaker in Microgrid with survival mode and parent Distribution
                # system has no failed lines
                if self.network.mode == "survival":
                    if self.network.distribution_network.failed_line:
                        self.network.connected_line.circuitbreaker.close()
                else:
                    self.network.connected_line.circuitbreaker.close()
        elif curr_time == 0:
            self.network.connected_line.circuitbreaker.close()

    def check_sensors(self, curr_time):
        connected_sections = [x for x in self.network.sections if x.connected]
        disconnected_sections = [
            x for x in self.network.sections if not x.connected
        ]
        for section in disconnected_sections:
            if curr_time > self.prev_open_time:
                if (
                    sum(
                        [
                            x.sensor.get_line_fail_status()
                            for x in section.disconnectors
                        ]
                    )
                    == 0
                ):
                    section.connect()
        for section in connected_sections:
            if (
                sum(
                    [
                        x.sensor.get_line_fail_status()
                        for x in section.disconnectors
                    ]
                )
                > 0
            ):
                self.prev_open_time = curr_time
                self.prev_section_time = curr_time
                self.remaining_section_time = self.section_time
                section.disconnect()

    def run_control_loop(self, curr_time):
        self.check_circuitbreaker(curr_time)
        self.check_sensors(curr_time)

    def check_lines_manually(self, curr_time):
        connected_sections = [x for x in self.network.sections if x.connected]
        disconnected_sections = [
            x for x in self.network.sections if not x.connected
        ]
        for section in disconnected_sections:
            if curr_time > self.prev_open_time:
                if sum([x.failed for x in section.lines]) == 0:
                    section.connect_manually()
        for section in connected_sections:
            if sum([x.failed for x in section.lines]) > 0:
                self.prev_open_time = curr_time
                self.prev_section_time = curr_time
                self.remaining_section_time = self.section_time
                section.disconnect_manually()

    def run_manual_control_loop(self, curr_time):
        self.check_circuitbreaker(curr_time)
        self.check_lines_manually(curr_time)

    def update_fail_status(self):
        pass

    def update_history(self, curr_time, save_flag: bool):
        if save_flag:
            self.history["remaining_section_time"][
                curr_time
            ] = self.remaining_section_time
            self.history["prev_section_time"][
                curr_time
            ] = self.prev_section_time

    def get_history(self, attribute: str):
        return self.history[attribute]

    def add_random_seed(self, random_gen):
        pass

    def print_status(self):
        pass

    def reset_status(self, save_flag: bool):
        self.prev_open_time = 0
        self.prev_section_time = 0
        self.remaining_section_time = 0
        if save_flag:
            self.initialize_history()

    def initialize_history(self):
        self.history["remaining_section_time"] = {}
        self.history["prev_section_time"] = {}
