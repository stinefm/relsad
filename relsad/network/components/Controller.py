from abc import ABC, abstractmethod
from enum import Enum

from relsad.Time import Time


class ControllerState(Enum):
    """
    Controller state

    Attributes
    ----------
    OK : int
        The controller is up and running
    SOFTWARE_FAIL : int
        A software fail has occurred
    HARDWARE_FAIL : int
        A hardware fail has occurred
    REPAIR : int
        The controller is being repaired
    """

    OK = 1
    SOFTWARE_FAIL = 2
    HARDWARE_FAIL = 3
    REPAIR = 4


class Controller(ABC):
    @abstractmethod
    def run_control_loop(self, curr_time: Time, dt: Time):
        pass
