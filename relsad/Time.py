from enum import Enum


class TimeUnit(Enum):
    SECOND = 1
    MINUTE = 2
    HOUR = 3
    DAY = 4
    WEEK = 5
    MONTH = 6
    YEAR = 7


class Time:

    """
    Common class for time

    ...

    Attributes
    ----------
    SEC_per_MIN : float
        Seconds in a minute
    MIN_per_HOUR : float
        Minutes in an hour
    HOUR_per_DAY : float
        Hours in a day
    DAY_per_WEEK : float
        Days in a week
    WEEK_per_MONTH : float
        Weeks in a month
    MONTH_per_YEAR : float
        Months in a year
    quantity : int
        Time quantity, the number of a time unit
    unit : TimeUnit
        The time unit

    Methods
    ----------
    convert_unit(unit)
        Converts the time based on the sat time unit to the correct time
    get_unit_quantity(unit)
    get_seconds()
        Returns the time in seconds
    get_minutes()
        Returns the time in minutes
    get_hours()
        Returns the time in hours
    get_days()
        Returns the time in days
    get_months()
        Returns the time in months
    get_years()
        Returns the time in year

    """

    SEC_per_MIN = 60
    MIN_per_HOUR = 60
    HOUR_per_DAY = 24
    DAY_per_WEEK = 7
    WEEK_per_MONTH = 4.3452
    MONTH_per_YEAR = 12

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
        elif self.unit == TimeUnit.DAY:
            return f"DAY_{self.quantity}"
        elif self.unit == TimeUnit.WEEK:
            return f"WEEK_{self.quantity}"
        elif self.unit == TimeUnit.MONTH:
            return f"MONTH_{self.quantity}"
        elif self.unit == TimeUnit.YEAR:
            return f"YEAR_{self.quantity}"

    def __repr__(self):
        if self.unit == TimeUnit.SECOND:
            return f"SEC_{self.quantity}"
        elif self.unit == TimeUnit.MINUTE:
            return f"MIN_{self.quantity}"
        elif self.unit == TimeUnit.HOUR:
            return f"HOUR_{self.quantity}"
        elif self.unit == TimeUnit.DAY:
            return f"DAY_{self.quantity}"
        elif self.unit == TimeUnit.WEEK:
            return f"WEEK_{self.quantity}"
        elif self.unit == TimeUnit.MONTH:
            return f"MONTH_{self.quantity}"
        elif self.unit == TimeUnit.YEAR:
            return f"YEAR_{self.quantity}"

    def __hash__(self):
        if self.unit == TimeUnit.SECOND:
            return hash(f"SEC_{self.quantity}")
        elif self.unit == TimeUnit.MINUTE:
            return hash(f"MIN_{self.quantity}")
        elif self.unit == TimeUnit.HOUR:
            return hash(f"HOUR_{self.quantity}")
        elif self.unit == TimeUnit.DAY:
            return hash(f"DAY_{self.quantity}")
        elif self.unit == TimeUnit.WEEK:
            return hash(f"WEEK_{self.quantity}")
        elif self.unit == TimeUnit.MONTH:
            return hash(f"MONTH_{self.quantity}")
        elif self.unit == TimeUnit.YEAR:
            return hash(f"YEAR_{self.quantity}")

    def convert_unit(self, unit: TimeUnit):
        """
        Converts the time based on the sat time unit to the correct time

        Parameters
        ----------
        unit : TimeUnit
            The time unit

        Returns
        ----------
        None

        """
        if unit == TimeUnit.SECOND:
            self.quantity = self.get_seconds()
            self.unit = TimeUnit.SECOND
        elif unit == TimeUnit.MINUTE:
            self.quantity = self.get_minutes()
            self.unit = TimeUnit.MINUTE
        elif unit == TimeUnit.HOUR:
            self.quantity = self.get_hours()
            self.unit = TimeUnit.HOUR
        elif unit == TimeUnit.DAY:
            self.quantity = self.get_days()
            self.unit = TimeUnit.DAY
        elif unit == TimeUnit.WEEK:
            self.quantity = self.get_weeks()
            self.unit = TimeUnit.WEEK
        elif unit == TimeUnit.MONTH:
            self.quantity = self.get_months()
            self.unit = TimeUnit.MONTH
        elif unit == TimeUnit.YEAR:
            self.quantity = self.get_years()
            self.unit = TimeUnit.YEAR

    def get_unit_quantity(self, unit: TimeUnit):
        """
        Converts the time based on the sat time unit to the correct time

        Parameters
        ----------
        unit : TimeUnit
            The time unit

        Returns
        ----------
        None

        """
        if unit == TimeUnit.SECOND:
            return self.get_seconds()
        elif unit == TimeUnit.MINUTE:
            return self.get_minutes()
        elif unit == TimeUnit.HOUR:
            return self.get_hours()
        elif unit == TimeUnit.DAY:
            return self.get_days()
        elif unit == TimeUnit.WEEK:
            return self.get_weeks()
        elif unit == TimeUnit.MONTH:
            return self.get_months()
        elif unit == TimeUnit.YEAR:
            return self.get_years()

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
        return self.get_hours() / other.get_hours()

    def get_seconds(self):
        """
        Returns the time in seconds

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return self.quantity
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity * self.SEC_per_MIN
        elif self.unit == TimeUnit.HOUR:
            return self.quantity * self.SEC_per_MIN * self.MIN_per_HOUR
        elif self.unit == TimeUnit.DAY:
            return (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
            )
        elif self.unit == TimeUnit.WEEK:
            return (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.MONTH:
            return (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.YEAR:
            return (
                self.quantity
                * self.SEC_per_MIN
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )

    def get_minutes(self):
        """
        Returns the time in minutes

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return self.quantity / self.SEC_per_MIN
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity
        elif self.unit == TimeUnit.HOUR:
            return self.quantity * self.MIN_per_HOUR
        elif self.unit == TimeUnit.DAY:
            return self.quantity * self.MIN_per_HOUR * self.HOUR_per_DAY
        elif self.unit == TimeUnit.WEEK:
            return (
                self.quantity
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.MONTH:
            return (
                self.quantity
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.YEAR:
            return (
                self.quantity
                * self.MIN_per_HOUR
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )

    def get_hours(self):
        """
        Returns the time in hours

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return self.quantity / self.SEC_per_MIN / self.MIN_per_HOUR
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity / self.MIN_per_HOUR
        elif self.unit == TimeUnit.HOUR:
            return self.quantity
        elif self.unit == TimeUnit.DAY:
            return self.quantity * self.HOUR_per_DAY
        elif self.unit == TimeUnit.WEEK:
            return self.quantity * self.HOUR_per_DAY * self.DAY_per_WEEK
        elif self.unit == TimeUnit.MONTH:
            return (
                self.quantity
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.YEAR:
            return (
                self.quantity
                * self.HOUR_per_DAY
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )

    def get_days(self):
        """
        Returns the time in days

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
            )
        elif self.unit == TimeUnit.MINUTE:
            return self.quantity / self.MIN_per_HOUR / self.HOUR_per_DAY
        elif self.unit == TimeUnit.HOUR:
            return self.quantity / self.HOUR_per_DAY
        elif self.unit == TimeUnit.DAY:
            return self.quantity
        elif self.unit == TimeUnit.WEEK:
            return self.quantity * self.DAY_per_WEEK
        elif self.unit == TimeUnit.MONTH:
            return self.quantity * self.DAY_per_WEEK * self.WEEK_per_MONTH
        elif self.unit == TimeUnit.YEAR:
            return (
                self.quantity
                * self.DAY_per_WEEK
                * self.WEEK_per_MONTH
                * self.MONTH_per_YEAR
            )

    def get_weeks(self):
        """
        Returns the time in weeks

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.MINUTE:
            return (
                self.quantity
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
            )
        elif self.unit == TimeUnit.HOUR:
            return self.quantity / self.HOUR_per_DAY / self.DAY_per_WEEK
        elif self.unit == TimeUnit.DAY:
            return self.quantity / self.DAY_per_WEEK
        elif self.unit == TimeUnit.WEEK:
            return self.quantity
        elif self.unit == TimeUnit.MONTH:
            return self.quantity * self.WEEK_per_MONTH
        elif self.unit == TimeUnit.YEAR:
            return self.quantity * self.WEEK_per_MONTH * self.MONTH_per_YEAR

    def get_months(self):
        """
        Returns the time in months

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.MINUTE:
            return (
                self.quantity
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.HOUR:
            return (
                self.quantity
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
            )
        elif self.unit == TimeUnit.DAY:
            return self.quantity / self.DAY_per_WEEK / self.WEEK_per_MONTH
        elif self.unit == TimeUnit.WEEK:
            return self.quantity / self.WEEK_per_MONTH
        elif self.unit == TimeUnit.MONTH:
            return self.quantity
        elif self.unit == TimeUnit.YEAR:
            return self.quantity * self.MONTH_per_YEAR

    def get_years(self):
        """
        Returns the time in years

        Parameters
        ----------
        None

        Returns
        ----------
        None

        """
        if self.unit == TimeUnit.SECOND:
            return (
                self.quantity
                / self.SEC_per_MIN
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.MINUTE:
            return (
                self.quantity
                / self.MIN_per_HOUR
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.HOUR:
            return (
                self.quantity
                / self.HOUR_per_DAY
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.DAY:
            return (
                self.quantity
                / self.DAY_per_WEEK
                / self.WEEK_per_MONTH
                / self.MONTH_per_YEAR
            )
        elif self.unit == TimeUnit.WEEK:
            return self.quantity / self.WEEK_per_MONTH / self.MONTH_per_YEAR
        elif self.unit == TimeUnit.MONTH:
            return self.quantity / self.MONTH_per_YEAR
        elif self.unit == TimeUnit.YEAR:
            return self.quantity


class TimeStamp:
    """
    Common class for time stamp

    ...

    Attributes
    ----------
    year : int
        Number of years
    month : int
        Number of months
    day : int
        Number of days
    hour : int
        Number of hours
    minute : int
        Number of minutes
    second : int
        Number of seconds

    Methods
    ----------
    get_hour_of_day(time_passed)

    """

    def __init__(
        self,
        year: int = 0,
        month: int = 0,
        day: int = 0,
        hour: int = 0,
        minute: int = 0,
        second: int = 0,
    ):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        self.second = second

    def __str__(self):
        return (
            f"TIMESTAMP_Y{self.year}-"
            + f"M{self.month}-"
            + f"D{self.day}_"
            + f"H{self.hour}:"
            + f"M{self.month}:"
            + f"S{self.second}"
        )

    def __repr__(self):
        return (
            f"TIMESTAMP_Y{self.year}-"
            + f"M{self.month}-"
            + f"D{self.day}_"
            + f"H{self.hour}:"
            + f"M{self.minute}:"
            + f"S{self.second}"
        )

    def __hash__(self):
        return hash(
            f"TIMESTAMP_Y{self.year}-"
            + f"M{self.month}-"
            + f"D{self.day}_"
            + f"H{self.hour}:"
            + f"M{self.minute}:"
            + f"S{self.second}"
        )

    def get_hour_of_day(self, time_passed: Time):
        """
        Returns the hour of day

        Parameters
        ----------
        time_passed : Time
            Time that have passed to the given hour of day

        Returns
        ----------
        None

        """
        if not isinstance(time_passed, Time):
            raise Exception("Wrong type")
        dup = Time(time_passed.quantity, time_passed.unit)
        if dup.get_years() > 1:
            y = int(dup.get_years())
            dup -= Time(y, TimeUnit.YEAR)
        if dup.get_months() > 1:
            m = int(dup.get_months())
            dup -= Time(m, TimeUnit.MONTH)
        if dup.get_days() > 1:
            d = int(dup.get_days())
            dup -= Time(d, TimeUnit.DAY)
        dup -= Time(self.hour, TimeUnit.HOUR)
        return int(dup.get_hours())

    def __sub__(self, other):
        if not isinstance(other, self.__class__):
            raise Exception("Wrong type")
        return (
            Time(self.year - other.year, TimeUnit.YEAR)
            + Time(self.month - other.month, TimeUnit.MONTH)
            + Time(self.day - other.day, TimeUnit.DAY)
            + Time(self.hour - other.hour, TimeUnit.HOUR)
            + Time(self.minute - other.minute, TimeUnit.MINUTE)
            + Time(self.second - other.second, TimeUnit.SECOND)
        )


if __name__ == "__main__":
    t1 = Time(5, TimeUnit.MINUTE)
    print(t1.get_years())
    print(t1.get_hours())
    t2 = Time(1, TimeUnit.HOUR)
    print(t2.get_years())
    print(t2.get_hours())
