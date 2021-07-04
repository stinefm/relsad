from abc import ABC, abstractmethod
from stinetwork.network.components import Bus, Line


class Network(ABC):

    # Enforce bus-list as attribute
    buses: list = None

    # Enforce line-list as attribute
    lines: list = None

    @abstractmethod
    def add_bus(self, bus: Bus):
        pass

    @abstractmethod
    def add_buses(self, buses: list):
        pass

    @abstractmethod
    def add_line(self, line: Line):
        pass

    @abstractmethod
    def add_lines(self, lines: list):
        pass

    @abstractmethod
    def get_lines(self):
        pass

    @abstractmethod
    def reset_slack_bus(self):
        pass
