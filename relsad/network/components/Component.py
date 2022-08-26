from abc import ABC, abstractmethod

from relsad.Time import Time


class Component(ABC):
    @abstractmethod
    def update_fail_status(self, dt: Time):
        pass

    @abstractmethod
    def update_history(
        self, prev_time: Time, curr_time: Time, save_flag: bool
    ):
        pass

    @abstractmethod
    def get_history(self, attribute: str):
        pass

    @abstractmethod
    def add_random_instance(self, random_gen):
        pass

    @abstractmethod
    def print_status(self):
        pass

    @abstractmethod
    def reset_status(self, save_flag: bool):
        pass
