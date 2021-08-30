from enum import Enum
import matplotlib.lines as mlines
import numpy as np
from .Component import Component
from stinetwork.utils import random_choice


class ManualController(Component):
    def __init__(
        self,
        name: str,
        section_time,
    ):

        self.name = name
        self.section_time
        self.power_system = None

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"ManualController(name={self.name})"

    def __eq__(self, other):
        if hasattr(other, "name"):
            return self.name == other.name and isinstance(
                other, ManualController
            )
        else:
            return False

    def __hash__(self):
        return hash(self.name)

    def run_control_loop(self, curr_time):
        for line in self.power_system.lines:
            if line.failed and line.connected:
                for disconnector in line.section.disconnectors:
                    disconnector.open(curr_time)
            elif not line.failed and not line.connected:
                for disconnector in line.section.disconnectors:
                    disconnector.close(curr_time)

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
