from abc import ABC, abstractmethod

from .Line import Line


class Switch(ABC):

    # Enforce line-list as attribute
    line: Line = None

    @abstractmethod
    def open(self):
        pass

    @abstractmethod
    def close(self):
        pass
