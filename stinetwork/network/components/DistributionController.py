from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from .MainController import ControllerState
from stinetwork.utils import random_choice


class DistributionController(Component):
    def __init__(
        self,
        name: str,
        network,
        fail_rate: float = 0,
        outage_time: float = 1,
        state: ControllerState = ControllerState.OK,
        section_time: float = 1,
    ):

        self.name = name
        self.fail_rate = fail_rate
        self.outage_time = outage_time
        self.state = state
        self.section_time = section_time
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
                other, DistributionController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def run_control_loop(self, curr_time):
        if (
            self.network.connected_line.circuitbreaker.is_open
            and self.remaining_section_time == 0
        ):
            self.remaining_section_time = self.section_time
            self.prev_section_time = curr_time
        elif (
            self.network.connected_line.circuitbreaker.is_open
            and curr_time > self.prev_section_time
        ) or curr_time == 0:
            if self.remaining_section_time >= 1:
                self.remaining_section_time -= 1
            if self.remaining_section_time == 0:
                self.network.connected_line.circuitbreaker.close()
        for sensor in self.sensors:
            if (
                sensor.get_line_fail_status() is True
                and sensor.get_line_connection_status() is True
            ):
                section = sensor.get_section()
                self.prev_open_time = curr_time
                self.prev_section_time = curr_time
                self.remaining_section_time = self.section_time
                for disconnector in section.disconnectors:
                    disconnector.router.open()
            elif (
                sensor.get_line_fail_status() is False
                and sensor.get_line_connection_status() is False
                and not self.network.connected_line.circuitbreaker.is_open
            ):
                section = sensor.get_section()
                if section:
                    for disconnector in section.disconnectors:
                        # Close disconnector one condition is met
                        if (
                            curr_time > self.prev_open_time
                            or disconnector.line.is_backup
                            or curr_time == 0
                        ):
                            disconnector.router.close()

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
