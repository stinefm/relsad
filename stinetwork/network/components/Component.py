from abc import ABC, abstractmethod


class Component(ABC):
    @abstractmethod
    def update_fail_status(self):
        pass

    @abstractmethod
    def update_history(self, prev_time, curr_time, save_flag: bool):
        pass

    @abstractmethod
    def get_history(self, attribute: str):
        pass

    @abstractmethod
    def add_random_seed(self, random_gen):
        pass

    @abstractmethod
    def print_status(self):
        pass

    @abstractmethod
    def reset_status(self, save_flag: bool):
        pass
