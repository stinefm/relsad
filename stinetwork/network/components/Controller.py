from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from stinetwork.utils import random_choice


class ControllerState(Enum):
    OK = 1
    FAILED = 2


class Controller(Component):
    def __init__(
        self,
        name: str,
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

        self.sensors = list()

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"Controller(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(other, Controller)
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def run_control_loop(self, curr_time):
        for sensor in self.sensors:
            if (
                sensor.get_line_fail_status is True
                and sensor.get_line_connection_status is True
            ):
                section = sensor.get_section()
                for disconnector in section.disconnectors:
                    disconnector.router.open_disconnector(curr_time)
            elif (
                sensor.get_line_fail_status is False
                and sensor.get_line_connection_status is False
            ):
                section = sensor.get_section()
                for disconnector in section.disconnectors:
                    disconnector.router.close_disconnector(curr_time)

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
