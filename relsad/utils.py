"""
This module contains package utils
"""

from enum import Enum
import numpy as np


def unique(sequence):
    """
    Return list of unique elements while preserving the order
    """
    seen = set()
    return [x for x in sequence if not (x in seen or seen.add(x))]


def subtract(list1, list2):
    """
    Return difference between lists while preserving the order
    """
    return [x for x in list1 if x not in list2]


def intersection(list1, list2):
    """
    Returns the intersection between two list while preserving the order
    """
    return [x for x in list1 if x in list2]


def random_instance(seed=None):
    """
    Return a numpy random instance with optional seed
    """
    return np.random.default_rng(seed)


def eq(x: float, y: float, tol: float = 1e-6):
    """
    Checks for equality within a tolerance
    """
    return abs(x - y) < tol


def random_choice(random_instance: np.random.Generator, p_true: float):
    """
    Returns random choice based on uniform probability distribution
    """
    return random_instance.random() < p_true


def interpolate(array: np.ndarray, time_indices: np.ndarray):
    return np.interp(time_indices, np.arange(array.size), array)


class TimeUnit(Enum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3


class Time:
    def __init__(self, quantity: int, unit: TimeUnit = TimeUnit.HOUR):
        self.quantity = quantity
        self.unit = unit

    def __str__(self):
        if self.unit == TimeUnit.SECOND:
            return f"SEC_{self.quantity}"
        elif self.unit == TimeUnit.MINUTE:
            return f"MIN_{self.quantity}"
        elif self.unit == TimeUnit.HOUR:
            return f"HOUR_{self.quantity}"

    def __repr__(self):
        if self.unit == TimeUnit.SECOND:
            return f"SEC_{self.quantity}"
        elif self.unit == TimeUnit.MINUTE:
            return f"MIN_{self.quantity}"
        elif self.unit == TimeUnit.HOUR:
            return f"HOUR_{self.quantity}"

    def __hash__(self):
        if self.unit == TimeUnit.SECOND:
            return hash(f"SEC_{self.quantity}")
        elif self.unit == TimeUnit.MINUTE:
            return hash(f"MIN_{self.quantity}")
        elif self.unit == TimeUnit.HOUR:
            return hash(f"HOUR_{self.quantity}")

    def convert_unit(self, unit: TimeUnit):
        if unit == TimeUnit.SECOND:
            self.quantity = self.get_seconds()
            self.unit = TimeUnit.SECOND
        elif unit == TimeUnit.MINUTE:
            self.quantity = self.get_minutes()
            self.unit = TimeUnit.MINUTE
        elif unit == TimeUnit.HOUR:
            self.quantity = self.get_hours()
            self.unit = TimeUnit.HOUR

    def get_unit_quantity(self, unit: TimeUnit):
        if unit == TimeUnit.SECOND:
            return self.get_seconds()
        elif unit == TimeUnit.MINUTE:
            return self.get_minutes()
        elif unit == TimeUnit.HOUR:
            return self.get_hours()

    def __lt__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity < other.get_unit_quantity(self.unit)

    def __le__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity <= other.get_unit_quantity(self.unit)

    def __gt__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity > other.get_unit_quantity(self.unit)

    def __ge__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity >= other.get_unit_quantity(self.unit)

    def __eq__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity == other.get_unit_quantity(self.unit)

    def __ne__(self, other):
        return isinstance(
            other, self.__class__
        ) and self.quantity != other.get_unit_quantity(self.unit)

    def __add__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return Time(
            self.quantity + other.get_unit_quantity(self.unit), self.unit
        )

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return Time(
            self.quantity - other.get_unit_quantity(self.unit), self.unit
        )

    def __truediv__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return Time(self.get_hours() / other.get_hours(), self.unit)

    def __mul__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        if self.unit == TimeUnit.SECOND:
            return Time(self.get_seconds() * other.quantity, self.unit)
        elif self.unit == TimeUnit.MINUTE:
            return Time(self.get_minutes() * other.quantity, self.unit)
        elif self.unit == TimeUnit.HOUR:
            return Time(self.get_hours() * other.quantity, self.unit)

    def get_hours(self):
        if self.unit == TimeUnit.SECOND:
            return self.quantity / (60 * 60)
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity / 60
        elif self.unit == TimeUnit.HOUR:
            return self.quantity

    def get_minutes(self):
        if self.unit == TimeUnit.SECOND:
            return self.quantity / 60
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity
        elif self.unit == TimeUnit.HOUR:
            return self.quantity * 60

    def get_seconds(self):
        if self.unit == TimeUnit.SECOND:
            return self.quantity
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity * 60
        elif self.unit == TimeUnit.HOUR:
            return self.quantity * 60 * 60


def convert_yearly_fail_rate(fail_rate_per_year: float, dt: Time):
    return fail_rate_per_year * dt.get_hours() / (365 * 24)


if __name__ == "__main__":
    pass
