from abc import ABC, abstractmethod
from enum import Enum
from relsad.Time import Time


class ControllerState(Enum):
    OK = 1
    SOFTWARE_FAIL = 2
    HARDWARE_FAIL = 3
    REPAIR = 4


class Controller(ABC):
    @abstractmethod
    def run_control_loop(self, curr_time: Time, dt: Time):
        pass